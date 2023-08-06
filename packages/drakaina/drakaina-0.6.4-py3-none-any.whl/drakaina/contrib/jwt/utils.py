from __future__ import annotations

import re
from datetime import datetime
from datetime import timedelta

try:
    from datetime import UTC
except ImportError:
    from datetime import tzinfo

    UTC = tzinfo(timedelta(minutes=0))  # noqa

from typing import Any
from typing import Iterable
from typing import Optional
from uuid import uuid4

from jwt import get_unverified_header
from jwt import InvalidAlgorithmError
from jwt import InvalidTokenError
from jwt import PyJWKClient
from jwt.api_jwt import decode_complete

from drakaina.contrib.jwt.errors import InvalidJWTTokenError
from drakaina.contrib.jwt.errors import JWTBackendError
from drakaina.contrib.jwt.errors import ValidationJWTTokenError
from drakaina.utils import iterable_str_arg


def datetime_utc_now() -> datetime:
    """Returns the current date/time in the UTC time zone.

    :return: The current date/time is in the UTC time zone.

    """
    return datetime.now(tz=UTC)


def datetime_to_timestamp(dt: datetime) -> int:
    """Converts the specified date/time to unixtime timestamp.

    :param dt: Date/time for conversion.
    :return: Unixtime timestamp.

    """
    return int(dt.timestamp())


def datetime_from_timestamp(ts: int) -> datetime:
    """Converts the specified unixtime timestamp to the python date/time type.

    :param ts: Timestamp for conversion.
    :return: Date/time from timestamp.

    """
    return datetime.fromtimestamp(ts, tz=UTC)


# Claims of specification JWT


def set_issuer(payload: dict[str, Any], value: str, claim: str = "iss"):
    """Sets the issuer of the token.

    https://tools.ietf.org/html/rfc7519#section-4.1.1

    :param payload: Token payload.
    :param value: Value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = value


def set_subject(payload: dict[str, Any], value: str, claim: str = "sub"):
    """Sets the subject of the token.

    https://tools.ietf.org/html/rfc7519#section-4.1.2

    :param payload: Token payload.
    :param value: Value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = value


def set_audience(payload: dict[str, Any], value: str, claim: str = "aud"):
    """Sets the audience of the token.

    https://tools.ietf.org/html/rfc7519#section-4.1.3

    :param payload: Token payload.
    :param value: Value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = value


def set_expiration(
    payload: dict[str, Any],
    now: datetime,
    lifetime: timedelta,
    claim: str = "exp",
):
    """Sets the expiration time of a token.

    https://tools.ietf.org/html/rfc7519#section-4.1.4

    :param payload: Token payload.
    :param now: Current date/time value to set the claim.
    :param lifetime: The value of the token lifetime to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = datetime_to_timestamp(now + lifetime)


def set_not_before(
    payload: dict[str, Any],
    activation_time: datetime,
    claim: str = "nbf",
):
    """Sets the time `Not before`.

    https://tools.ietf.org/html/rfc7519#section-4.1.5

    :param payload: Token payload.
    :param activation_time: Date/time value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = datetime_to_timestamp(activation_time)


def set_issued_at(payload: dict[str, Any], now: datetime, claim: str = "iat"):
    """Sets the time of token issuance.

    https://tools.ietf.org/html/rfc7519#section-4.1.6

    :param payload: Token payload.
    :param now: Current date/time value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = datetime_to_timestamp(now)


def set_token_id(
    payload: dict[str, Any],
    value: Optional[str] = None,
    claim: str = "jti",
):
    """Sets the token identifier.

    https://tools.ietf.org/html/rfc7519#section-4.1.7

    :param payload: Token payload.
    :param value: Value to set the claim. Default UUID4.
    :param claim: Claim short name (key).

    """
    payload[claim] = value if value else uuid4().hex


def check_expiration(
    payload: dict[str, Any],
    now: datetime,
    claim: str = "exp",
):
    """Checks if the timestamp value has passed in the given claim
    (since the given time value in `now`).
    If yes, it causes a `InvalidTokenError` with an error message.

    :param payload: Token payload.
    :param now: Current date/time value to check the claim.
    :param claim: Claim short name (key).

    :raise InvalidJWTTokenError:
    :raise ValidationJWTTokenError:

    """
    try:
        expiration_value = payload[claim]
    except KeyError:
        raise InvalidJWTTokenError(f"Token has no `{claim}` claim")

    expiration = datetime_from_timestamp(expiration_value)
    if now >= expiration:
        raise ValidationJWTTokenError(f"Token `{claim}` claim has expired")


def check_not_before(
    payload: dict[str, Any],
    now: datetime,
    claim: str = "nbf",
):
    """Checks if the timestamp value has reached the specified claim
    (the moment of the specified `now` time value).
    If so, raises a `InvalidTokenError` with an error message.

    :param payload: Token payload.
    :param now: Current date/time value to check the claim.
    :param claim: Claim short name (key).

    :raise InvalidJWTTokenError:
    :raise ValidationJWTTokenError:

    """
    try:
        not_before_value = payload[claim]
    except KeyError:
        raise InvalidJWTTokenError(f"Token has no `{claim}` claim")

    not_before_value = datetime_from_timestamp(not_before_value)
    if now < not_before_value:
        raise ValidationJWTTokenError(f"Token `{claim}` claim not reached")


# Custom JWT claims


def set_token_type(payload: dict[str, Any], value: str, claim: str = "jtt"):
    """Sets the token type claim.

    :param payload: Token payload.
    :param value: Value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = value


def set_permission_scopes(
    payload: dict[str, Any],
    scopes: str | Iterable[str],
    claim: str = "scp",
):
    """Sets the claim of the permissions scopes.

    :param payload: Token payload.
    :param scopes: Value to set the claim.
    :param claim: Claim short name (key).

    """
    payload[claim] = ",".join(iterable_str_arg(scopes))


# Token handlers


def decode_jwt_token(
    token: str,
    algorithms: Iterable[str],
    signing_key: str,
    verify_key: str,
    verify: bool = True,
    decode_options: dict[bool | list[str]] = None,
    verify_values: dict[str, str | Iterable[str] | re.Pattern | None] = None,
    leeway: int | float = 0,
    jwk_url: Optional[str] = None,
) -> dict[str, Any]:
    """Performs validation of the provided token and returns
    its payload dictionary.

    :param token: JWT token.
    :param algorithms: Supported algorithms.
    :param signing_key: Signing key if used symmetric algorithm.
    :param verify_key: Public key if used asymmetric algorithm.
    :param verify: Verify token.
    :param decode_options: Options argument for `pyjwt.decode`.
        Example:
        `{
            "require": ["iss", "exp", "jti"],
            "verify_iss": False,
            "verify_exp": True,
            "verify_jti": False,
        }`
    :param verify_values: Values to be verified.
    :param leeway: Leeway time in seconds.
    :param jwk_url: URL for the PyJWK client.
        It gets the validation key for the specified jwt-token.
    :return: Decoded JWT token payload.

    :raise JWTBackendError: In the case of incorrectly passed
        parameters and arguments.
    :raise ValidationJWTTokenError: In case the token has an invalid signature
        or invalid payload data.

    """

    header = get_unverified_header(token)
    if header["alg"].startswith("HS"):
        verifying_key = signing_key
    elif jwk_url:
        jwks_client = PyJWKClient(jwk_url)
        verifying_key = jwks_client.get_signing_key_from_jwt(token).key
    else:
        verifying_key = verify_key

    verify_values = {} if verify_values is None else verify_values.copy()
    options = {"verify_signature": verify, **decode_options}
    params = {"leeway": leeway}

    # Provide values to check in the pyjwt module
    if "verify_iss" in options and options["verify_iss"] is True:
        # Issuer - One
        params["issuer"] = verify_values.pop("iss")
    if "verify_aud" in options and options["verify_aud"] is True:
        # Audience - One or Many
        if isinstance(verify_values.get("aud"), (str, list)):
            params["audience"] = verify_values.pop("aud")
        else:
            # todo: will be validate in `_extra_validation`
            options["verify_aud"] = False

    try:
        token_data = decode_complete(
            jwt=token,
            key=verifying_key,
            algorithms=algorithms,
            options=options,
            verify=verify,
            **params,
        )
    except InvalidAlgorithmError as error:
        raise JWTBackendError("Invalid algorithm specified") from error
    except InvalidTokenError:
        raise ValidationJWTTokenError("Token is invalid or expired")

    if verify:
        _extra_validation(token_data, verify_values)

    return token_data["payload"]


def _extra_validation(
    decoded_token: dict[str, dict[str, Any] | str],
    verify_values: dict[str, str | Iterable[str] | re.Pattern] = None,
):
    """Performs an additional check that is not performed by the pyjwt module.

    The check is performed by comparing the data provided for the check with
    the data included in the token payload with the same keys.

    :param decoded_token: Dict returned from `pyjwt.decode_complete`. Must
        contain a `header' and `payload'.
    :param verify_values: Dict with data to be validated. The keys must match
        the dictionary fields with the token payload.
    :raise ValidationJWTTokenError: In case the token has an invalid
        payload or header data.

    """
    header = decoded_token["header"]
    verify_header_values = verify_values.pop("header", [])
    payload = decoded_token["payload"]

    try:
        for key, value in verify_header_values:
            token_value = header.get(key)
            if isinstance(value, (str, int)):
                assert value == token_value
            elif isinstance(value, Iterable):
                assert token_value in value
            elif isinstance(value, re.Pattern):
                assert re.match(value, token_value)
    except AssertionError as error:
        raise ValidationJWTTokenError("Invalid token header") from error

    try:
        for key, value in verify_values:
            token_value = payload.get(key)
            if isinstance(value, (str, int)):
                assert value != token_value
            elif isinstance(value, Iterable):
                assert token_value not in value
            elif isinstance(value, re.Pattern):
                assert value.match(token_value)
    except AssertionError as error:
        raise ValidationJWTTokenError("Invalid token payload") from error
