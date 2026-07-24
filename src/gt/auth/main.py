from fastapi import FastAPI

from .models import (
    AuthUserModel,
    AuthUserOnboardingModel,
)


class Auth:
    """
    Auth class for authentication and authorization.
    """

    def __init__(
        self,
        *,
        base,
        user_model: type[AuthUserModel],
        user_onboarding_model: type[AuthUserOnboardingModel],
        # database_async_session: AsyncSession,
    ):
        """
        Initialize the Auth class.
        """

        if not base:
            raise ValueError("Base must be provided")

        if not user_model or not issubclass(user_model, AuthUserModel):
            raise ValueError("user_model must be an instance of AuthUserModel")

        if not user_onboarding_model or not issubclass(
            user_onboarding_model, AuthUserOnboardingModel
        ):
            raise ValueError(
                "user_onboarding_model must be an instance of AuthUserOnboardingModel"
            )

        self.user_model = user_model
        self.user_onboarding_model = user_onboarding_model

        # self.database_async_session = database_async_session

    def init_app(self, app: FastAPI):
        """
        Initialize the FastAPI application with the Auth class.
        """
        from .routers.router_registry import register_auth_routers

        register_auth_routers(app)
