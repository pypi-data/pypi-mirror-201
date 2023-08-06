from __future__ import annotations

from collections.abc import Awaitable
from collections.abc import Callable
from collections.abc import Mapping
from collections.abc import MutableMapping
from collections.abc import MutableSequence
from collections.abc import Sequence
from sys import version_info
from typing import Any
from typing import Iterable
from typing import Type
from typing import Union

if version_info >= (3, 8):
    from typing import Literal
    from typing import Protocol
    from typing import TypedDict
else:
    from typing_extensions import Literal
    from typing_extensions import Protocol
    from typing_extensions import TypedDict

if version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired


"""
JSON-RPC types definitions
"""

JSONSimpleTypes = Union[str, int, float, bool, None]
JSONTypes = Union[
    JSONSimpleTypes,
    Mapping[str, JSONSimpleTypes],
    Sequence[JSONSimpleTypes],
]


class JSONRPCRequestObject(TypedDict):
    jsonrpc: Literal["2.0"]
    method: str
    params: NotRequired[list[JSONTypes] | dict[str, JSONTypes]]
    id: NotRequired[str | int | None]


class JSONErrorObject(TypedDict):
    code: int
    message: str
    data: NotRequired[JSONTypes]


class JSONRPCResponseObject(TypedDict):
    jsonrpc: Literal["2.0"]
    result: NotRequired[JSONTypes]
    error: NotRequired[JSONErrorObject]
    id: str | int | None


JSONRPCBatchRequestObject = Sequence[JSONRPCRequestObject]
JSONRPCRequest = Union[JSONRPCRequestObject, JSONRPCBatchRequestObject]
JSONRPCBatchResponseObject = Sequence[JSONRPCResponseObject]
JSONRPCResponse = Union[JSONRPCResponseObject, JSONRPCBatchResponseObject]


"""
WSGI types definitions
PEP 3333 – Python Web Server Gateway Interface
https://peps.python.org/pep-3333/
"""

WSGIEnvironmentKeys = Literal[
    # for CGI
    # https://datatracker.ietf.org/doc/html/draft-coar-cgi-v11-03
    "AUTH_TYPE",
    "CONTENT_LENGTH",
    "CONTENT_TYPE",
    "GATEWAY_INTERFACE",
    "PATH_INFO",
    "PATH_TRANSLATED",
    "QUERY_STRING",
    "REMOTE_ADDR",
    "REMOTE_HOST",
    "REMOTE_IDENT",
    "REMOTE_USER",
    "REQUEST_METHOD",
    "SCRIPT_NAME",
    "SERVER_NAME",
    "SERVER_PORT",
    "SERVER_PROTOCOL",
    "SERVER_SOFTWARE",
    # for WSGI
    "wsgi.errors",
    "wsgi.input",
    "wsgi.multiprocess",
    "wsgi.multithread",
    "wsgi.run_once",
    "wsgi.url_scheme",
    "wsgi.version",
]
# for framework needs
WSGIDrakainaKeys = Literal[
    "drakaina.app",
    "drakaina.is_authenticated",
]
WSGIEnvironment = MutableMapping[str, Any]
WSGIExceptionInfo = tuple[Type[BaseException], BaseException, Any]


class WSGIStartResponse(Protocol):
    def __call__(
        self,
        status: str,
        headers: MutableSequence[tuple[str, str]],
        exc_info: WSGIExceptionInfo | None = ...,
    ) -> Callable[[bytes], Any]:
        ...


WSGIResponse = Iterable[bytes]
WSGIApplication = Callable[[WSGIEnvironment, WSGIStartResponse], WSGIResponse]


class WSGIInputStream(Protocol):
    def read(self, size: int | None = None) -> bytes:
        ...

    def readline(self) -> bytes:
        ...

    def readlines(self, hint: Any | None) -> Iterable[bytes]:
        ...

    def __iter__(self) -> bytes:
        ...


class WSGIErrorsStream(Protocol):
    def flush(self) -> None:
        ...

    def write(self, s: str) -> None:
        ...

    def writelines(self, seq: Sequence[str]) -> None:
        ...


"""
ASGI types definitions
"""

ASGIScope = MutableMapping[str, Any]
ASGIMessage = MutableMapping[str, Any]

ASGIReceive = Callable[[], Awaitable[ASGIMessage]]
ASGISend = Callable[[ASGIMessage], Awaitable[None]]

ASGIApplication = Callable[[ASGIScope, ASGIReceive, ASGISend], Awaitable[None]]


"""
Helpful types
"""


class Comparator(Protocol):
    def __call__(
        self,
        required: Iterable[str],
        provided: str | Iterable[str],
    ) -> bool:
        ...


class ProxyRequest(MutableMapping):
    """A wrapper class for environment mapping.

    :param environment:

    """

    __slots__ = ("__environment",)

    def __init__(self, environment: ASGIScope | WSGIEnvironment):
        self.__environment = environment

    def __getitem__(self, item):
        return self.__environment[item]

    def __setitem__(self, key, value):
        self.__environment[key] = value

    def __delitem__(self, key):
        del self.__environment[key]

    def __iter__(self):
        return iter(self.__environment.keys())

    def __contains__(self, item):
        return item in self.__environment.keys()

    def __len__(self):
        return len(self.__environment)

    def keys(self):
        return self.__environment.keys()

    def values(self):
        return self.__environment.values()

    def items(self):
        return self.__environment.items()

    def get(self, key, default=None):
        return self.__environment.get(key, default)

    def clear(self):
        self.__environment.clear()

    def setdefault(self, key, default=None):
        self.__environment.setdefault(key, default)

    def pop(self, key, default=None):
        return self.__environment.pop(key, default)

    def popitem(self):
        return self.__environment.popitem()

    def copy(self):
        return self.__class__(self.__environment.copy())

    def update(self, *args, **kwargs):
        return self.__environment.update(*args, **kwargs)

    def __getattr__(self, item):
        if item in ["__environment", "_ProxyRequest__environment"]:
            super().__getattribute__(item)
        return self.__environment[item]

    def __setattr__(self, key, value):
        if key in ["__environment", "_ProxyRequest__environment"]:
            super().__setattr__(key, value)
        else:
            self.__environment[key] = value

    def __delattr__(self, item):
        del self.__environment[item]


AnyRequest = Union[ASGIScope, WSGIEnvironment, ProxyRequest]
