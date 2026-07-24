from .main import Auth

__all__ = ["Auth"]


def __getattr__(name):
    if name == "Auth":
        return Auth
    raise AttributeError(f"module {__name__} has no attribute {name}")
