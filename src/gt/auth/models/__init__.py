from ._auth_user_account_model import create_auth_user_account_model
from ._auth_user_model import AuthUserModel
from ._auth_user_onboarding_model import AuthUserOnboardingModel
from ._auth_user_session_model import create_auth_user_session_model
from ._auth_user_tokens_model import create_auth_user_tokens_model

__all__ = [
    "AuthUserModel",
    "AuthUserOnboardingModel",
    "create_auth_user_account_model",
    "create_auth_user_session_model",
    "create_auth_user_tokens_model",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
