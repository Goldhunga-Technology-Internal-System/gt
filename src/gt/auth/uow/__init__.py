from ._auth_uow import AuthUOW

__all__ = ["AuthUOW"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
