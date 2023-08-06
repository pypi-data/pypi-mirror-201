from __future__ import annotations

from functools import partial
from logging import Logger
from typing import Iterable
from typing import Optional
from typing import Type
from typing import Union

from drakaina import ENV_APP
from drakaina._types import WSGIApplication
from drakaina._types import WSGIEnvironment
from drakaina._types import WSGIInputStream
from drakaina._types import WSGIResponse
from drakaina._types import WSGIStartResponse
from drakaina.exceptions import BadRequestError
from drakaina.middleware.base import BaseMiddleware
from drakaina.middleware.exception import ExceptionMiddleware
from drakaina.middleware.request_wrapper import RequestWrapperMiddleware
from drakaina.rpc_protocols import BaseRPCProtocol
from drakaina.rpc_protocols import JsonRPCv2

ALLOWED_METHODS = ("OPTIONS", "GET", "POST")
Middlewares = Iterable[Type[BaseMiddleware] | partial[BaseMiddleware]]


class WSGIHandler:
    """Implementation of WSGI protocol.

    :param route:
    :type route: str
    :param handler: RPC protocol implementation.
    :type handler: BaseRPCProtocol
    :param middlewares: List of WSGI middlewares.
    :type middlewares: Iterable[Type[BaseMiddleware] | partial[BaseMiddleware]]
    :param logger: A `logging.Logger` object.
    :type logger: Logger
    :param max_content_size: Limiting request body size for DoS protection.
    :type max_content_size: int
    :param provide_smd:
    :type provide_smd: bool | str
    :param provide_openrpc:
    :type provide_openrpc: bool | str
    :param provide_openapi:
    :type provide_openapi: bool | str

    """

    __slots__ = (
        "environ",
        "start_response",
        "handler",
        "route",
        "logger",
        "max_content_size",
        "provide_smd",
        "provide_openrpc",
        "provide_openapi",
        "_rpc_content_type",
        "_allowed_methods",
        "_middlewares_chain",
    )

    environ: WSGIEnvironment
    start_response: WSGIStartResponse
    _middlewares_chain: Union[WSGIApplication, BaseMiddleware]

    def __init__(
        self,
        route: Optional[str] = None,
        handler: Optional[BaseRPCProtocol] = None,
        middlewares: Optional[Middlewares] = None,
        logger: Optional[Logger] = None,
        max_content_size: int = 4096,
        provide_smd: Optional[Union[bool, str]] = False,
        provide_openrpc: Optional[Union[bool, str]] = False,
        provide_openapi: Optional[Union[bool, str]] = False,
    ):
        self.handler = handler if handler is not None else JsonRPCv2()
        self._rpc_content_type = self.handler.content_type

        self.route = route
        if isinstance(self.route, str) and not self.route.startswith("/"):
            self.route = "/" + self.route

        self.logger = logger
        self.max_content_size = int(max_content_size)
        self.provide_smd = provide_smd
        self.provide_openrpc = provide_openrpc
        self.provide_openapi = provide_openapi

        if provide_smd or provide_openrpc or provide_openapi:
            self._allowed_methods = ", ".join(ALLOWED_METHODS)
        else:
            self._allowed_methods = ", ".join(
                [m for m in ALLOWED_METHODS if m != "GET"],
            )

        # Build middleware stack
        self._middlewares_chain = self._wsgi_app
        kw = {"is_async": False}
        for mw in reversed(middlewares or []):
            if (
                isinstance(mw, partial)
                and issubclass(mw.func, BaseMiddleware)
                or issubclass(mw, BaseMiddleware)
            ):
                self._middlewares_chain = mw(self._middlewares_chain, **kw)
            self._middlewares_chain = mw(self._middlewares_chain)

        # The middleware for handling exceptions in the middleware according
        #  to the RPC protocol.
        self._middlewares_chain = ExceptionMiddleware(
            RequestWrapperMiddleware(self._middlewares_chain, **kw),  # noqa
            handler=self.handler,
            logger=self.logger,
            **kw,
        )

    def __call__(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        environ[ENV_APP] = self
        return self._middlewares_chain(environ, start_response)  # noqa

    def _wsgi_app(
        self,
        environ: WSGIEnvironment,
        start_response: WSGIStartResponse,
    ) -> WSGIResponse:
        self.environ = environ
        self.start_response = start_response

        method = environ["REQUEST_METHOD"]
        if method in ALLOWED_METHODS:
            if self._validate_path(environ["PATH_INFO"]):
                return getattr(self, method.lower())()

            return self._not_found()

        return self._method_not_allowed()

    def get(self) -> WSGIResponse:
        if self.provide_smd:
            response_body = self.handler.smd_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
        elif self.provide_openrpc:
            response_body = self.handler.openrpc_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
        elif self.provide_openapi:
            response_body = self.handler.openapi_scheme()
            response_headers = [
                ("Content-Type", "application/json"),
                ("Content-Length", str(len(response_body))),
            ]
        else:
            return self._method_not_allowed()

        self.start_response("200 OK", response_headers)
        return (response_body,)

    def post(self) -> WSGIResponse:
        wsgi_input: WSGIInputStream = self.environ["wsgi.input"]

        content_type = self.environ.get("CONTENT_TYPE")
        content_length = int(self.environ.get("CONTENT_LENGTH") or 0)
        if (
            not (content_type and content_length)
            or content_type != self._rpc_content_type
            or content_length > self.max_content_size
        ):
            if content_type != self._rpc_content_type:
                response_status = "415 Unsupported Media Type"
            else:
                response_status = "400 Bad Request"
            # Return RPC error
            response_body = self.handler.get_raw_error(BadRequestError())
        else:
            response_status = "200 OK"
            response_body = self.handler.handle_raw_request(
                wsgi_input.read(content_length),
                request=self.environ,
            )

        response_headers = [
            ("Content-Type", self._rpc_content_type),
            ("Content-Length", str(len(response_body))),
        ]
        self.start_response(response_status, response_headers)

        yield response_body

    def options(self) -> WSGIResponse:
        response_headers = [
            ("Allow", self._allowed_methods),
            ("Content-Length", "0"),
        ]
        self.start_response("200 OK", response_headers)
        yield b""

    def _not_found(self) -> WSGIResponse:
        response_headers = []
        self.start_response("404 Not Found", response_headers)
        yield b""

    def _method_not_allowed(self) -> WSGIResponse:
        response_headers = [("Allow", self._allowed_methods)]
        self.start_response("405 Method Not Allowed", response_headers)
        yield b""

    def _validate_path(self, path_info: str) -> bool:
        return (
            self.route is not None
            and isinstance(path_info, str)
            and path_info.startswith(self.route)
        )
