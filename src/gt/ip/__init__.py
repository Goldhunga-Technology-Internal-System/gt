from ._ip_service import IPService

__all__ = ["IPService"]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module {__name__} has no attribute {name}")
