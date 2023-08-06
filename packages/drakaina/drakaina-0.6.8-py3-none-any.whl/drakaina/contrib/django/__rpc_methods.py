from typing import Dict

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.http import HttpRequest

from drakaina import remote_procedure
from drakaina.exceptions import AuthenticationFailedError
from drakaina.contrib.jwt.utils import decode_jwt_token
from drakaina.contrib.jwt.utils import get_tokens_for
from drakaina.contrib.jwt.utils import refresh_tokens

UserModel = get_user_model()
UPDATE_LAST_LOGIN = True
ROTATE_REFRESH_TOKENS = False


def get_user(request: HttpRequest, username: str, password: str) -> UserModel:
    authenticate_kwargs = {
        UserModel.USERNAME_FIELD: username,
        "password": password,
        "request": request,
    }
    user = authenticate(**authenticate_kwargs)

    if user is None or not user.is_active:
        raise AuthenticationFailedError(
            "No active account found with the given credentials",
        )

    return user


@remote_procedure(name="token", provide_request=True)
def get_token(
    request: HttpRequest,
    username: str,
    password: str,
) -> Dict[str, str]:
    user = get_user(request, username, password)

    tokens = get_tokens_for(user.id)

    if UPDATE_LAST_LOGIN:
        update_last_login(None, user)

    return tokens


@remote_procedure(name="token.refresh")
def refresh_token(refresh: str) -> Dict[str, str]:
    return refresh_tokens(
        refresh,
        verify=True,
        rotate_refresh=ROTATE_REFRESH_TOKENS,
    )


@remote_procedure(name="token.verify")
def verify_token(token: str) -> bool:
    decode_jwt_token(token, [], "", "")
    return True
