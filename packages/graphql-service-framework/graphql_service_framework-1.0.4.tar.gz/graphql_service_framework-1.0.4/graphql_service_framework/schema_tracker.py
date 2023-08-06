import functools
import importlib
import inspect
import os

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Type, List

from graphql import print_schema

from schemadiff import diff
from schemadiff.changes.field import FieldDescriptionChanged
from schemadiff.formatting import format_change_by_criticality

from graphql_service_framework.schema import Schema
from graphql_service_framework.utils import \
    increment_version, \
    install_package, \
    find_modules, \
    find_schema, \
    get_py_code_changes, \
    set_api_version


@dataclass
class SchemaTracker:
    name: str
    path: str
    schema: Type[Schema]

    @classmethod
    def find_schemas(
            cls,
            path,
            package_name,
            index_url
    ) -> List['SchemaTracker']:

        schema_trackers = []
        for folder in os.listdir(path):
            full_path = os.path.join(path, folder)
            if os.path.isdir(full_path) and not folder.startswith(".") and \
                    folder not in ["tests"]:
                schema_name = folder

                if modules := find_modules(full_path, schema_name):
                    if schema := find_schema(modules):
                        schema_trackers.append(
                            SchemaTracker(
                                name=schema_name,
                                path=full_path,
                                schema=schema,
                                package_name=package_name,
                                index_url=index_url
                            )
                        )

        return schema_trackers

    def __init__(
            self,
            schema: Type[Schema],
            name: str,
            path: str,
            package_name: str,
            index_url: str
    ):
        self.schema = schema
        self.name = name
        self.path = path
        self.package_name = package_name
        self.index_url = index_url

    def __hash__(self):
        return hash((self.name, self.path))

    @functools.cache
    def previous_schema(self) -> Optional[Type[Schema]]:
        print(f"Checking for a previous version of {self.name}")
        _prev_report = install_package(self.name, index_url=self.index_url)

        if _prev_report:
            v = _prev_report['install'][0]['metadata']['version']

            install_location = _prev_report.get("pip_show").get('Location')
            print(
                f"Installed package "
                f"{self.name} version {v} at {install_location}"
            )

            prev_modules = find_modules(
                os.path.join(install_location, self.package_name, self.name),
                f"{self.package_name}.{self.name}"
            )

            return find_schema(prev_modules)

    @functools.cache
    def code_changes(self):
        if self.previous_schema():
            a_path = self.path
            b_path = os.path.dirname(
                importlib.import_module(
                    f"{self.package_name}.{self.name}"
                ).__file__
            )

            print(
                f"Comparing code for {self.name} with version "
                f"{self.previous_schema().api_version}\n"
                f"a_path={a_path}\nb_path={b_path}"
            )
            return get_py_code_changes(
                a_path,
                b_path,
                self.previous_schema().api_version
            )
        return None

    def changes(self):
        if not self.previous_schema():
            return []
        else:
            new_schema_language = print_schema(self.schema.graphql_schema())
            previous_schema_language = print_schema(
                self.previous_schema().graphql_schema()
            ).replace(f" {self.package_name}.", " ")

            return diff(
                previous_schema_language,
                new_schema_language
            )

    def change_log(self):
        prev_version = self.previous_schema().api_version \
            if self.previous_schema() else None

        version = f"**{self.version()}** (updated from *{prev_version}*)" \
            if prev_version and prev_version != self.version() else \
            f"*{self.version()}*"

        log = f"- {self.name} {version}\n"
        if not self.previous_schema():
            log += "  - *New Schema*\n"
        elif not self.changes() and self.code_changes():
            log += "  - *Code changes only* (No Schema changes)\n"
        elif self.major_changes_count() or \
                self.minor_changes_count() or \
                self.micro_changes_count():
            log += f"  - " \
                   f"{self.major_changes_count()} breaking, " \
                   f"{self.minor_changes_count()} safe, " \
                   f"{self.micro_changes_count()} micro Schema changes \n"
            for change in self.changes():
                log += f"    - {format_change_by_criticality(change)}\n"

        return log

    def major_changes_count(self):
        return sum(
            change.breaking or change.dangerous
            for change in self.changes()
        )

    def minor_changes_count(self):
        return sum(
            change.safe and not isinstance(change, FieldDescriptionChanged)
            for change in self.changes()
        )

    def micro_changes_count(self):
        count = sum(
            isinstance(change, FieldDescriptionChanged)
            for change in self.changes()
        )
        if not count and (self.code_changes() or not self.previous_schema()):
            count = 1

        return count

    def version(self):
        if not self.previous_schema():
            return "0.0.1"

        previous_version = self.previous_schema().api_version

        if self.major_changes_count():
            return increment_version(previous_version, 0)
        elif self.minor_changes_count():
            return increment_version(previous_version, 1)
        elif self.micro_changes_count():
            return increment_version(previous_version, 2)

        return previous_version

    def release(self):
        release_reason = None
        if not self.previous_schema():
            release_reason = "this is a new schema"
        elif self.changes():
            release_reason = "the schema has been changed"
        elif self.code_changes():
            release_reason = "the source code as been changed"

        if not release_reason:
            return

        print(f"Releasing {self.name} because {release_reason}")
        print(f"Schema: {print_schema(self.schema.graphql_schema())}")
        print(f"Creating setup.py in {self.path} for {self.name}")

        setup_data = inspect.cleandoc("""
            from setuptools import setup

            setup(
                name='SERVICE_NAME',
                version='SERVICE_VERSION',
                packages=['SERVICE_PACKAGE'],
                install_requires=[
                    'packaging',
                    'graphql-api',
                    'graphql-service-framework'
                ]
            )
            """) \
            .replace('SERVICE_NAME', self.name.replace("_", "-")) \
            .replace('SERVICE_VERSION', self.version()) \
            .replace('SERVICE_PACKAGE', f"{self.package_name}.{self.name}")

        with open(os.path.join(self.path, "setup.py"), 'w') as file:
            file.write(setup_data)

        print(f"Inserting api_version = {self.version()} into {self.name}")
        for file in Path(self.path).rglob("*.py"):
            file.write_text(set_api_version(file.read_text(), self.version()))
