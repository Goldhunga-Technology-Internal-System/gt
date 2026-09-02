from authlib.integrations.starlette_client import OAuth
from fastapi.requests import Request
from starlette.responses import RedirectResponse

from gt.auth.interfaces._oauth_provider_interface import IOAuthProvider, OAuthUserInfo


class GoogleOAuthProvider(IOAuthProvider):
    """
    Google OAuth Provider implementation.
    """

    def __init__(
        self, google_oauth_client_id: str, google_oauth_client_secret: str, app_url: str
    ):
        self.oauth = OAuth()
        self.app_url = app_url

        self.oauth.register(
            name="google",
            client_id=google_oauth_client_id,
            client_secret=google_oauth_client_secret,
            server_metadata_url=(
                "https://accounts.google.com/.well-known/openid-configuration"
            ),
            client_kwargs={"scope": "openid email profile"},
        )

        self.client = self.oauth.create_client("google")

    async def authorize_redirect(self, request: Request) -> RedirectResponse:
        """
        Get the authorization URL for Google OAuth.
        """

        redirect_uri = f"{self.app_url}/auth/oauth/callback/google"

        return await self.client.authorize_redirect(request, redirect_uri)

    async def get_user(self, request: Request) -> OAuthUserInfo:
        """
        Get the user information from Google OAuth.
         - Fetch the token using the authorization code.
         - Retrieve user information from Google using the token.
        """
        token = await self.client.authorize_access_token(request)
        user_info = token.get("userinfo")

        # Google may return email_verified as a bool or the string "true".
        email_verified = user_info.get("email_verified", False)
        if isinstance(email_verified, str):
            email_verified = email_verified.lower() == "true"

        return OAuthUserInfo(
            email=user_info["email"],
            provider_user_id=user_info["sub"],
            email_verified=bool(email_verified),
            name=user_info.get("name"),
            avatar_url=user_info.get("picture"),
        )
