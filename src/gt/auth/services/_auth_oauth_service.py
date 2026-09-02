from typing import Literal

from gt.auth.settings import AuthSettings
from gt.exceptions._base_exceptions import InvalidException


class AuthOAuthService:
    """
    Service class for handling OAuth authentication.
    """

    def __init__(
        self,
        settings: AuthSettings,
        provider: Literal["google"],
    ):
        """
        Initialize the AuthOAuthService with the specified provider.
        """
        self.provider: Literal["google"] = provider
        self.settings = settings

    def __post__init(self):
        """
        Post-initialization to validate the provider.
        """
        if not self.provider or self.provider not in ["google"]:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def _get_oauth_provider(
        self, client_id: str, client_secret: str, app_url: str
    ):
        """
        Get the OAuth provider instance based on the provider name.
        """
        from gt.auth.factory._oauth_factory import OAuthFactory

        return OAuthFactory.get_provider(
            provider_name=self.provider,
            client_id=client_id,
            client_secret=client_secret,
            app_url=app_url,
        )

    async def authorize_redirect(self, request):
        """
        Get the authorization URL for the specified OAuth provider.
        """

        if (
            not self.settings.google_oauth_client_id
            or not self.settings.google_oauth_client_secret
            or not self.settings.oauth_app_url
        ):
            raise InvalidException(
                error="Google OAuth client ID, client secret, or app URL is not configured. Please check your settings."
            )
        provider = await self._get_oauth_provider(
            client_id=self.settings.google_oauth_client_id,
            client_secret=self.settings.google_oauth_client_secret,
            app_url=self.settings.oauth_app_url,
        )
        return await provider.authorize_redirect(request)


def get_auth_oauth_service(
    *,
    settings: AuthSettings = AuthSettings(),
    provider: Literal["google"] = "google",
) -> AuthOAuthService:
    """
    Dependency function to get an instance of AuthOAuthService.
    """
    return AuthOAuthService(settings=settings, provider=provider)
