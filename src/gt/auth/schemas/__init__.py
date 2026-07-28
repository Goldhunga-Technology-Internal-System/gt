from ._auth_schemas import AuthUserRegisterSchema

__all__ = ["AuthUserRegisterSchema"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
