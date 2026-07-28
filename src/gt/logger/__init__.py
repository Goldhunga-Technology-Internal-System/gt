from ._base_logger import get_base_logger

logger = get_base_logger()

__all__ = ["logger"]


def __getattr__(name: str):
    if name == "logger":
        return logger
    raise AttributeError(f"module {__name__} has no attribute {name}")
