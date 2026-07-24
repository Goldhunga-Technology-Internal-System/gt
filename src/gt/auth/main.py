from .models import (
    AuthUserModel,
    AuthUserOnboardingModel,
    create_auth_user_account_model,
    create_auth_user_session_model,
    create_auth_user_tokens_model,
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
        self.user_account_model = create_auth_user_account_model(base, user_model)
        self.user_session_model = create_auth_user_session_model(base, user_model)
        self.user_tokens_model = create_auth_user_tokens_model(base, user_model)
