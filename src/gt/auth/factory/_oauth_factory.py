from typing import Literal

from gt.auth.interfaces._oauth_provider_interface import IOAuthProvider


class OAuthFactory:
    """
    Factory class for creating OAuth instances.
    """

    @staticmethod
    def get_provider(
        provider_name: Literal["google"],
        client_id: str,
        client_secret: str,
        app_url: str,
    ) -> IOAuthProvider:
        """
        Get the OAuth provider instance based on the provider name.
        """

        match provider_name:
            case "google":
                from gt.auth.adapters._google_oauth_provider import GoogleOAuthProvider

                return GoogleOAuthProvider(
                    google_oauth_client_id=client_id,
                    google_oauth_client_secret=client_secret,
                    app_url=app_url,
                )

            case _:
                raise ValueError(f"Unsupported OAuth provider: {provider_name}")
