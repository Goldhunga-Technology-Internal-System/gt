from ._auth_user_service import AuthUserService, get_auth_user_service

__all__ = ["AuthUserService", "get_auth_user_service"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
