from ._account.auth_user_account_model import create_auth_user_account_model
from ._onboarding.auth_user_onboarding_model import AuthUserOnboardingModel
from ._session.auth_user_session_model import create_auth_user_session_model
from ._tokens.auth_user_tokens_model import create_auth_user_tokens_model
from ._user.auth_user_model import AuthUserModel

__all__ = [
    "AuthUserModel",
    "AuthUserOnboardingModel",
    "create_auth_user_account_model",
    "create_auth_user_session_model",
    "create_auth_user_tokens_model",
]


def __getattr__(name):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")
