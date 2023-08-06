from collections.abc import Callable
from inspect import getfullargspec
from typing import Any
from typing import Dict
from typing import Iterator
from typing import Optional
from typing import Tuple

from drakaina.utils import unwrap_func

__all__ = (
    "is_rpc_procedure",
    "RPCRegistry",
    "RPC_REGISTRY",
    "RPC_NAME",
    "RPC_REGISTERED",
    "RPC_PROVIDE_REQUEST",
    "RPC_META",
)

# Reserved procedure argument names
RESERVED_KWARGS = ("self", "request")

# RPC procedure fields
RPC_REGISTRY = "__rpc_registry"
RPC_NAME = "__rpc_name"
RPC_REGISTERED = "__rpc_procedure"
RPC_PROVIDE_REQUEST = "__rpc_provide_request"
RPC_META = "__rpc_metadata"


def is_rpc_procedure(func: Callable) -> bool:
    return hasattr(unwrap_func(func), RPC_REGISTERED)


class RPCRegistry:
    """Registry of remote procedures"""

    _remote_procedures: Dict[str, Callable[..., Any]]

    def __init__(self):
        self._remote_procedures = {}

    def register_procedure(
        self,
        procedure: Callable[..., Any],
        name: Optional[str] = None,
        provide_request: Optional[bool] = None,
        metadata: Optional[dict] = None,
    ):
        """Register a function as a remote procedure.

        :param procedure:
            Registered procedure.
        :type procedure: Callable
        :param name:
            Procedure name. Default as function name.
        :type name: str
        :param provide_request:
            If `True`, then the request object or context can be supplied to
            the procedure as a `request` argument.
        :type provide_request: bool
        :param metadata:
            Metadata that can be processed by middleware.
        :type metadata: dict

        """
        assert callable(procedure)

        procedure_name = procedure.__name__ if name is None else name
        # The loop is for applying attributes to wrapped functions.
        # If the provided function is not wrapped, the attributes will be
        # applied once
        _func = procedure
        while _func is not None:
            setattr(_func, RPC_REGISTRY, self)
            setattr(_func, RPC_NAME, procedure_name)
            setattr(_func, RPC_REGISTERED, True)
            setattr(_func, RPC_PROVIDE_REQUEST, provide_request)
            setattr(_func, RPC_META, metadata or {})
            # If it's a wrapped function
            _func = getattr(_func, "__wrapped__", None)

        procedure.__rpc_args = [
            a
            for a in getfullargspec(procedure).args
            if a not in RESERVED_KWARGS
        ]

        self._remote_procedures[procedure_name] = procedure

    def replace(self, procedure: Callable, new_procedure: Callable):
        procedure_name = getattr(procedure, RPC_NAME, None)
        self._remote_procedures[procedure_name] = new_procedure

    def __getitem__(self, key: str) -> Optional[Callable]:
        return self._remote_procedures.get(key)

    def __setitem__(self, key: str, value: Callable):
        self.register_procedure(procedure=value, name=key)

    def __delitem__(self, key: str):
        del self._remote_procedures[key]

    def __len__(self) -> int:
        return len(self._remote_procedures)

    def __iter__(self) -> Iterator[str]:
        yield self._remote_procedures

    def get(
        self,
        key: str,
        default: Optional[Callable] = None,
    ) -> Optional[Callable]:
        return self._remote_procedures.get(key, default)

    def items(self) -> Iterator[Tuple[str, Callable]]:
        yield self._remote_procedures.items()
