from typing import Any
from typing import Optional
from typing import Union

from drakaina._types import JSONRPCRequest
from drakaina._types import JSONRPCRequestObject
from drakaina._types import JSONRPCResponse
from drakaina._types import JSONRPCResponseObject
from drakaina.exceptions import AuthenticationFailedError
from drakaina.exceptions import BadRequestError
from drakaina.exceptions import DeserializationError
from drakaina.exceptions import ForbiddenError
from drakaina.exceptions import InternalServerError
from drakaina.exceptions import InvalidParametersError
from drakaina.exceptions import InvalidPermissionsError
from drakaina.exceptions import InvalidTokenError
from drakaina.exceptions import NotFoundError
from drakaina.exceptions import RPCError
from drakaina.exceptions import SerializationError
from drakaina.registries import RPCRegistry
from drakaina.rpc_protocols.base import BaseRPCProtocol
from drakaina.serializers import BaseSerializer
from drakaina.serializers import JsonSerializer


class JsonRPCError(RPCError):
    """JSON-RPC Common error

    Reserved for implementation-defined server-errors.
    Codes -32000 to -32099.

    """

    code: int = -32000
    default_message: str = "Server error"
    id: Union[int, str] = None
    data: Any = None

    def __init__(
        self,
        *args,
        message: str = None,
        id: Union[int, str] = None,
        data: Optional[Any] = None,
    ):
        super().__init__(*args)

        self.id = id
        if message:
            self.message = message

        if self.message and data:
            self.data = {"text": self.message.strip(), "details": data}
        elif self.message:
            self.data = self.message.strip()
        elif data:
            self.data = data

    def __str__(self) -> str:
        return f"{self.__class__.__name__} ({self.code} {self.default_message})"

    def as_dict(self) -> JSONRPCResponseObject:
        error = dict(
            jsonrpc="2.0",
            error={"code": self.code, "message": self.default_message},
            id=self.id,
        )

        if self.data:
            error["error"]["data"] = self.data

        return error


class InvalidRequestError(JsonRPCError):
    """Invalid Request

    The JSON sent is not a valid Request object.

    """

    code = -32600
    default_message = "Invalid Request"


class MethodNotFoundError(JsonRPCError):
    """Method not found

    The method does not exist / is not available.

    """

    code = -32601
    default_message = "Method not found"


class InvalidParamsError(JsonRPCError):
    """Invalid params

    Invalid method parameter(s).

    """

    code = -32602
    default_message = "Invalid params"


class InternalError(JsonRPCError):
    """Internal error

    Internal JSON-RPC error.

    """

    code = -32603
    default_message = "Internal error"


class ParseError(JsonRPCError):
    """Parse error

    Invalid JSON was received by the server.
    An error occurred on the server while parsing the JSON text.

    """

    code = -32700
    default_message = "Parse error"


# Implementation of Drakaina errors


class AuthenticationFailedJRPCError(JsonRPCError):
    """Authentication failed"""

    code = -32010
    default_message = "Authentication failed"


class InvalidTokenJRPCError(AuthenticationFailedJRPCError):
    """Invalid token error"""

    code = -32011
    default_message = "Invalid token error"


class ForbiddenJRPCError(AuthenticationFailedJRPCError):
    """Forbidden error"""

    code = -32012
    default_message = "Forbidden"


class InvalidPermissionsJRPCError(ForbiddenJRPCError):
    """Invalid permissions error"""

    code = -32013
    default_message = "Invalid permissions error"


class JsonRPCv2(BaseRPCProtocol):
    """JSON-RPC 2.0 implementation.

    :param registry:
        Registry of remote procedures.
        Default: `drakaina.registries.rpc_registry` (generic module instance)
    :type registry: RPCRegistry
    :param serializer:
        Serializer object. Default: `JsonSerializer` (stdlib.json)
    :type serializer: BaseSerializer

    """

    def __init__(
        self,
        registry: Optional[RPCRegistry] = None,
        serializer: Optional[BaseSerializer] = None,
    ):
        if serializer is None:
            serializer = JsonSerializer()
        super().__init__(registry=registry, serializer=serializer)

        self._errors_map = {
            Exception: JsonRPCError,
            RPCError: JsonRPCError,
            BadRequestError: InvalidRequestError,
            NotFoundError: MethodNotFoundError,
            InvalidParametersError: InvalidParamsError,
            InternalServerError: InternalError,
            SerializationError: InternalError,
            DeserializationError: ParseError,
            AuthenticationFailedError: AuthenticationFailedJRPCError,
            InvalidTokenError: InvalidTokenJRPCError,
            ForbiddenError: ForbiddenJRPCError,
            InvalidPermissionsError: InvalidPermissionsJRPCError,
        }

    def handle(
        self,
        rpc_request: JSONRPCRequest,
        request: Optional[Any] = None,
    ) -> Optional[JSONRPCResponse]:
        """Handles a procedure call or batch of procedure call

        :param rpc_request:
            RPC request in protocol format.
        :type rpc_request: JSONRPCRequest
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure.
        :type request: Any
        :return:
            Returns the result in protocol format.
        :rtype: JSONRPCResponse

        """
        # Check bad request
        if not (isinstance(rpc_request, (dict, list)) and len(rpc_request) > 0):
            return InvalidRequestError().as_dict()

        # Handle batch request
        if isinstance(rpc_request, list):
            batch_result = []
            for request_object in rpc_request:
                result = self.execute(request_object, request=request)
                if result is not None:
                    batch_result.append(result)
            if len(batch_result) == 0:
                return None
            return batch_result

        # Handle single request
        return self.execute(rpc_request, request=request)

    def execute(
        self,
        procedure_call: JSONRPCRequestObject,
        request: Optional[Any] = None,
    ) -> Optional[JSONRPCResponseObject]:
        """Execute a remote procedure call.

        :param procedure_call:
            RPC request object in protocol format.
        :type procedure_call: JSONRPCRequestObject
        :param request:
            Optional parameter that can be passed as an
            argument to the procedure. By default, None will be passed.
        :type request: Any
        :return:
            Returns a result object in protocol format.
        :rtype: JSONRPCResponseObject

        """
        if not isinstance(procedure_call, dict):
            return InvalidRequestError().as_dict()
        method: str = procedure_call.get("method")
        params: Optional[Union[list, dict]] = procedure_call.get("params")
        request_id: Optional[Union[int, str]] = procedure_call.get("id")

        # Validate protocol
        if (
            procedure_call.get("jsonrpc") != "2.0"
            or not isinstance(method, str)
            or not (params is None or isinstance(params, (list, dict)))
            or not (request_id is None or isinstance(request_id, (int, str)))
        ):
            return InvalidRequestError(id=request_id).as_dict()

        # Getting procedure
        procedure = self.registry[method]
        if procedure is None:
            if request_id is None:
                return None
            return MethodNotFoundError(id=request_id).as_dict()

        # Prepare parameters
        args, kwargs = (), {}
        if params is not None:
            if isinstance(params, list):
                args = (request, *params)
            elif isinstance(params, dict):
                kwargs = dict(request=request, **params)
        else:
            kwargs = dict(request=request)

        # Execute RPC method
        try:
            result = procedure(*args, **kwargs)
        except JsonRPCError as err:
            err.id = request_id
            return err.as_dict()
        except Exception as err:
            return InternalError(message=str(err), id=request_id).as_dict()

        if request_id is None:
            return None

        return dict(jsonrpc="2.0", result=result, id=request_id)

    @property
    def base_error_class(self):
        return JsonRPCError

    @property
    def default_error_class(self):
        return InternalError

    def smd_scheme(self):
        return {}
