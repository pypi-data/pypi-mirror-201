from typing import Dict, Callable, Iterable

from context_helper import Context
from werkzeug import Request

from graphql_service_framework.mesh import ServiceManager, ServiceConnection
from graphql_service_framework.wsgi import WSGIApp


def add_mesh_middleware(app, config):
    relative_path = config.get("http_relative_path", "")

    service_management_path = config.get(
        "http_service_management_path",
        f"{relative_path}/service"
    )

    connections = []

    for key, service in config.get('services', {}).items():
        version = service.python_type.api_version.split('.')

        connection = ServiceConnection(
            name=key,
            schema=service.python_type,
            api_version_specifier=f"~={version[0]}.{version[1]}",
            service_url=service.executor.url
        )

        connections.append(connection)

    return ServiceMeshMiddleware(
        app,
        ServiceManager(
            name=config.get("service_name"),
            api_version=config.get("api_version"),
            connections=connections
        ),
        service_management_path=service_management_path
    )


class ServiceMeshMiddleware:

    def __init__(
            self,
            app: WSGIApp,
            service_manager: 'ServiceManager',
            service_management_path: str = None,
            check_connections_on_first_request: bool = True,
            context_key: str = "services"
    ):
        self.app = app
        self.service_manager = service_manager
        self.service_management_path = service_management_path
        self.connect_on_first_request = check_connections_on_first_request
        self.context_key = context_key

    def __call__(
            self,
            environ: Dict,
            start_response: Callable
    ) -> Iterable[bytes]:
        if self.connect_on_first_request:
            self.service_manager.connect()

        request = Request(environ)

        if request.path == f"{self.service_management_path}":
            # Expose the service management HTTP server
            return self.service_manager.management_http_server.app()(
                environ, start_response
            )

        with Context(**{self.context_key: self.service_manager}):
            return self.app(environ, start_response)
