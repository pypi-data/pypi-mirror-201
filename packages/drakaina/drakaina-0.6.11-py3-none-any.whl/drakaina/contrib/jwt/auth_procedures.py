from __future__ import annotations

from drakaina import remote_procedure
from drakaina.config import rpc_config
from drakaina.contrib.jwt.utils import get_tokens_for
from drakaina.contrib.jwt.utils import get_tokens_by
from drakaina.contrib.jwt.utils import GetNewUserID
from drakaina.contrib.jwt.utils import GetUserID
from drakaina.contrib.jwt.utils import verify_jwt_token
from drakaina.exceptions import AuthenticationFailedError


get_user_id: GetUserID = None
get_new_user_id: GetNewUserID = None


@remote_procedure(name="token", provide_request=True)
def token(request, form_data: dict[str, str]) -> dict[str, str]:
    """todo: docstring"""
    # validate data
    user_id = get_user_id(form_data, request=request)
    if user_id is None:
        raise AuthenticationFailedError(  # todo
            "No active account found with the given credentials",
        )  # "Incorrect email or password"

    # generate tokens
    # RefreshToken, SlidingToken
    tokens = get_tokens_for(user_id)

    return tokens


@remote_procedure(name="register", provide_request=True)
def register(request, form_data: dict[str, str]) -> dict[str, str]:
    """todo: docstring"""
    """
    # Fast API Example
    @app.post("/signup", summary="Create new user", response_model=UserOut)
    async def create_user(data: UserAuth):
        # querying database to check if user already exist
        user = db.get(data.email, None)
        if user is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exist",
            )
        user = {
            "email": data.email,
            "password": get_hashed_password(data.password),
            "id": str(uuid4()),
        }
        db[data.email] = user  # saving user to database
        return user

    """
    # validate data
    user_id = get_new_user_id(form_data, request=request)
    if user_id is None:
        raise AuthenticationFailedError(  # todo
            "User with this email already exist",
        )

    # generate tokens
    # RefreshToken, SlidingToken
    tokens = get_tokens_for(user_id)

    return tokens


@remote_procedure(name="token.refresh", provide_request=True)
def refresh_token(refresh: str) -> dict[str, str]:
    """todo: docstring"""
    """
    class TokenRefreshSerializer("serializers.Serializer"):
        Takes a refresh type JSON web token and returns an access type JSON web
        token if the refresh token is valid.

        refresh = serializers.CharField()
        access = serializers.CharField(read_only=True)
        token_class = RefreshToken

        def validate(self, attrs):
            refresh = self.token_class(attrs["refresh"])

            data = {"access": str(refresh.access_token)}

            if api_settings.ROTATE_REFRESH_TOKENS:
                if api_settings.BLACKLIST_AFTER_ROTATION:
                    try:
                        # Attempt to blacklist the given refresh token
                        refresh.blacklist()
                    except AttributeError:
                        # If blacklist app not installed, `blacklist` method will
                        # not be present
                        pass

                refresh.set_jti()
                refresh.set_exp()
                refresh.set_iat()

                data["refresh"] = str(refresh)

            return data

    class TokenRefreshSlidingSerializer("serializers.Serializer"):
        Takes a sliding JSON web token and returns a new, refreshed version if the
        token's refresh period has not expired.

        token = serializers.CharField()
        token_class = "SlidingToken"

        def validate(self, attrs):
            token = self.token_class(attrs["token"])

            # Check that the timestamp in the "refresh_exp" claim has not
            # passed
            token.check_exp("SLIDING_TOKEN_REFRESH_EXP_CLAIM")

            # Update the "exp" and "iat" claims
            token.set_exp()
            token.set_iat()

            return {"token": str(token)}

    class TokenBlacklistSerializer("serializers.Serializer"):
        Takes a token and blacklists it. Must be used with the
        `rest_framework_simplejwt.token_blacklist` app installed.

        refresh = serializers.CharField()
        token_class = "RefreshToken"

        def validate(self, attrs):
            refresh = self.token_class(attrs["refresh"])
            try:
                refresh.blacklist()
            except AttributeError:
                pass
            return {}

    """
    return get_tokens_by(refresh, rpc_config.ROTATE_REFRESH_TOKENS)


@remote_procedure(name="token.verify", provide_request=True)
def verify_token(token: str) -> bool:
    """todo: docstring"""
    verify_jwt_token(token)
    return True
