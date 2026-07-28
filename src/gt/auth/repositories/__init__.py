from ._auth_user_repository import AuthUserRepository

__all__ = ["AuthUserRepository"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
