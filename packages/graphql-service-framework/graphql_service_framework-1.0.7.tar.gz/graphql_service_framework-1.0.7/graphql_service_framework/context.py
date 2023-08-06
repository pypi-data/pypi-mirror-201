from typing import Dict, Callable, Iterable

from context_helper import Context
from werkzeug import Request

from graphql_service_framework.manager import ServiceManager
from graphql_service_framework.wsgi import WSGIApp


class ServiceContextMiddleware:

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
