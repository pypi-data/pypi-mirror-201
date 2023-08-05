from __future__ import annotations

from asyncio import iscoroutinefunction
from functools import update_wrapper
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Optional
from typing import TypeVar

from drakaina._types import ASGIScope
from drakaina._types import Comparator
from drakaina._types import WSGIEnvironment
from drakaina.exceptions import AuthenticationFailedError
from drakaina.exceptions import ForbiddenError
from drakaina.registries import is_rpc_procedure
from drakaina.registries import RPCRegistry
from drakaina.utils import iterable_str_arg

__all__ = (
    "RPCRegistry",
    "rpc_registry",
    "remote_procedure",
    "check_permissions",
    "login_required",
    "match_all",
    "match_any",
    "ENV_APP",
    "ENV_IS_AUTHENTICATED",
    "ENV_USER",
    "ENV_USER_ID",
    "ENV_AUTH_PAYLOAD",
    "ENV_AUTH_SCOPES",
)

# General registry
rpc_registry = RPCRegistry()

# Environ (Request) context
ENV_APP = "drakaina.app"
ENV_IS_AUTHENTICATED = "auth.is_authenticated"
ENV_USER = "user"
ENV_USER_ID = "user_id"
ENV_AUTH_PAYLOAD = "auth.payload"
ENV_AUTH_SCOPES = "auth.scopes"

T = TypeVar("T")


def remote_procedure(
    name: Optional[str] = None,
    registry: Optional[RPCRegistry] = None,
    provide_request: Optional[bool] = None,
    metadata: Optional[dict[str, Any]] = None,
    **meta_options,
) -> Callable:
    """Decorator allow wrap function and define it as remote procedure.

    :param name:
        Procedure name. Default as function name.
    :type name: str
    :param registry:
        Procedure registry custom object
    :type registry: RPCRegistry
    :param provide_request:
        Provide a request object or context data (from the transport layer).
        If `True`, then the request object or context can be supplied to
        the procedure as a `request` argument.
    :type provide_request: bool
    :param metadata:
        Metadata that can be processed by middleware.
    :type metadata: dict[str, Any]
    :param meta_options:
        Metadata that can be processed by middleware.

    """

    def __decorator(
        procedure: T,
        _registry: RPCRegistry = None,
        _name: str = None,
        _provide_request: bool = None,
        **_meta_options,
    ) -> T:
        """Returns a registered procedure"""

        if iscoroutinefunction(procedure):

            async def wrapper(*args, **kwargs):
                if not _provide_request:
                    if len(args) == 0:
                        kwargs.pop("request")
                    else:
                        scope, *args = args
                return await procedure(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                if not _provide_request:
                    if len(args) == 0:
                        kwargs.pop("request")
                    else:
                        environ, *args = args
                return procedure(*args, **kwargs)

        # Need to update the wrapper before registering in the registry
        decorated_procedure = update_wrapper(wrapper, procedure)

        if _registry is None:
            _registry = rpc_registry
        if _name is None:
            _name = procedure.__name__
        _metadata = _meta_options.pop("metadata") or {}
        _registry.register_procedure(
            decorated_procedure,
            name=_name,
            provide_request=_provide_request,
            metadata={**_metadata, **_meta_options},
        )

        return decorated_procedure

    if callable(name):
        return __decorator(
            name,
            registry,
            None,
            provide_request,
            metadata=metadata,
            **meta_options,
        )
    elif not isinstance(name, (str, type(None))):
        raise TypeError(
            "Expected first argument to be an str, a callable, or None",
        )

    def decorator(procedure):
        assert callable(procedure)
        return __decorator(
            procedure,
            registry,
            name,
            provide_request,
            metadata=metadata,
            **meta_options,
        )

    return decorator


def login_required(*_args) -> Callable:
    """Requires login decorator.

    Gives access to the procedure only to authenticated users.

    """

    def __decorator(procedure: T) -> T:
        """Returns a registered procedure"""
        if not is_rpc_procedure(procedure):
            raise TypeError(
                "Incorrect usage of decorator. Please use "
                "the `drakaina.remote_procedure` decorator first.",
            )

        if iscoroutinefunction(procedure):

            async def wrapper(*args, **kwargs):
                if len(args) == 0:
                    scope: ASGIScope = kwargs.get("request")
                else:
                    scope: ASGIScope = args[0]

                if not scope.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return await procedure(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                if len(args) == 0:
                    environ: WSGIEnvironment = kwargs.get("request")
                else:
                    environ: WSGIEnvironment = args[0]

                if not environ.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")
                return procedure(*args, **kwargs)

        return update_wrapper(wrapper, procedure)

    if len(_args) > 0:
        if callable(_args[0]):
            return __decorator(_args[0])
        else:
            raise TypeError("Expected first argument to be a callable")

    def decorator(procedure):
        assert callable(procedure)
        return __decorator(procedure)

    return decorator


def match_any(
    required: Iterable[str],
    provided: str | Iterable[str],
) -> bool:
    return any((scope in provided for scope in required))


def match_all(
    required: Iterable[str],
    provided: str | Iterable[str],
) -> bool:
    return set(required).issubset(set(provided))


def check_permissions(
    scopes: str | Iterable[str],
    comparator: Comparator = match_all,
) -> Callable:
    """Permission decorator.

    Gives access to the procedure only to authorized users.

    """
    if not (
        isinstance(scopes, str)
        or (
            isinstance(scopes, Iterable)
            and all((isinstance(scope, str) for scope in scopes))
        )
    ):
        raise TypeError(
            "The `scopes` argument must be a string or Iterable[string]",
        )
    if not callable(comparator):
        raise TypeError(
            "The `comparator` argument must be a function that implements "
            "the Comparator interface",
        )

    procedure_scopes = iterable_str_arg(scopes)

    def __decorator(procedure: T) -> T:
        if not is_rpc_procedure(procedure):
            raise TypeError(
                "Incorrect usage of decorator. Please use "
                "the `drakaina.remote_procedure` decorator first.",
            )

        if iscoroutinefunction(procedure):

            async def wrapper(*args, **kwargs):
                if len(args) == 0:  # noqa
                    scope: ASGIScope = kwargs.get("request")
                else:
                    scope: ASGIScope = args[0]

                if not scope.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")

                user_scopes = _get_scopes(scope)
                if not isinstance(user_scopes, Iterable):
                    raise AuthenticationFailedError(
                        "Invalid permissions format",
                    )

                if not comparator(procedure_scopes, user_scopes):
                    raise ForbiddenError("Forbidden")

                return await procedure(*args, **kwargs)

        else:

            def wrapper(*args, **kwargs):
                if len(args) == 0:  # noqa
                    environ: WSGIEnvironment = kwargs.get("request")
                else:
                    environ: WSGIEnvironment = args[0]

                if not environ.get(ENV_IS_AUTHENTICATED, False):
                    raise ForbiddenError("Authorization required")

                user_scopes = _get_scopes(environ)
                if not isinstance(user_scopes, Iterable):
                    raise AuthenticationFailedError(
                        "Invalid permissions format",
                    )

                if not comparator(procedure_scopes, user_scopes):
                    raise ForbiddenError("Forbidden")

                return procedure(*args, **kwargs)

        return update_wrapper(wrapper, procedure)

    return __decorator


def _get_scopes(
    request: WSGIEnvironment | ASGIScope,
) -> Optional[Iterable[str]]:
    scopes = request.get(ENV_AUTH_SCOPES)
    if scopes:
        return iterable_str_arg(scopes)
