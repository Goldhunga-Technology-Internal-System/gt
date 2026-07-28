from ._auth_user_account_repository import AuthUserAccountRepository
from ._auth_user_repository import AuthUserRepository
from ._auth_user_session_repository import AuthUserSessionRepository

__all__ = [
    "AuthUserAccountRepository",
    "AuthUserRepository",
    "AuthUserSessionRepository",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
