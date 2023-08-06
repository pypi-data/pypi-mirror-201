from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from drakaina import rpc_registry
from drakaina.exceptions import InternalServerError
from drakaina.exceptions import RPCError
from drakaina.registries import RPCRegistry
from drakaina.serializers import BaseSerializer

__all__ = ("BaseRPCProtocol",)


class BaseRPCProtocol:
    """Base class for representing the remote procedure call (RPC) protocol.

    :param registry:
        Registry of remote procedures.
        Default: `drakaina.registries.rpc_registry` (generic module instance)
    :type registry: RPCRegistry
    :param serializer:
        Serializer object.
    :type serializer: BaseSerializer

    """

    __slots__ = ("registry", "serializer", "_errors_map")

    def __init__(
        self,
        registry: Optional[RPCRegistry] = None,
        serializer: Optional[BaseSerializer] = None,
    ):
        self.registry = registry if registry is not None else rpc_registry
        self.serializer = serializer

        self._errors_map = {Exception: RPCError}

    def handle_raw_request(
        self,
        raw_data: bytes,
        request: Optional[Any] = None,
    ) -> bytes:
        """Accepts raw data, serializes, processes the RPC request,
        and returns the deserialized result.

        :param raw_data:
            Raw request data.
        :type raw_data:
        :param request:
            Request object or context data. Can be provided to
            a remote procedure.
        :type request: Any
        :return:
            Deserialized RPC response data.

        """
        try:
            parsed_data = self.serializer.deserialize(raw_data)
        except Exception as exc:
            return self.get_raw_error(exc)

        response_data = self.handle(parsed_data, request=request)
        if response_data is None:
            return b""

        try:
            return self.serializer.serialize(response_data)
        except Exception as exc:
            return self.get_raw_error(exc)

    def get_raw_error(
        self,
        error: Union[RPCError, Exception, Type[Exception]],
    ) -> bytes:
        """Returns the deserialized error object.

        :param error:
            The instance or class of the error.
        :type error: RPCError | Type[RPCError] | Exception
        :return:
            Raw error data.

        """

        if isinstance(error, type) and issubclass(error, Exception):
            error = error()

        if isinstance(error, self.base_error_class):
            rpc_error = error
        else:
            rpc_error_class = self._errors_map.get(
                type(error),
                self.default_error_class,
            )
            rpc_error = rpc_error_class(str(error))

        return self.serializer.serialize(rpc_error.as_dict())

    def handle(self, rpc_request: Any, request: Optional[Any] = None) -> Any:
        """Handles a procedure call.

        :param rpc_request:
            RPC request in protocol format.
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure. By default, None will be passed.
        :return:
            Returns the result in protocol format.

        """
        raise NotImplementedError(
            "You must implement the `handle` method in the child class",
        )

    @property
    def base_error_class(self):
        return RPCError

    @property
    def default_error_class(self):
        return InternalServerError

    @property
    def content_type(self) -> str:
        return self.serializer.content_type

    def smd_scheme(self) -> bytes:
        raise NotImplementedError

    def openrpc_scheme(self) -> bytes:
        """Implementation of OpenRPC specification

        https://open-rpc.org/getting-started
        https://spec.open-rpc.org/#introduction
        """
        raise NotImplementedError

    def openapi_scheme(self) -> bytes:
        """Implementation of OpenAPI specification

        https://github.com/OAI/OpenAPI-Specification
        """
        raise NotImplementedError
