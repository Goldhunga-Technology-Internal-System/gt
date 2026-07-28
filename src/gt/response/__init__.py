from ._response import (
    CustomErrorResponseSchema,
    CustomSuccessResponseSchema,
)
from ._response import (
    CustomResponse as cr,
)

__all__ = ["CustomErrorResponseSchema", "CustomSuccessResponseSchema", "cr"]


def __getattr__(name):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
