from ._organization_schemas import (
    OrganizationCreateSchema,
    OrganizationMemberAddSchema,
    OrganizationMemberResponseSchema,
    OrganizationMemberUpdateSchema,
    OrganizationResponseSchema,
    OrganizationUpdateSchema,
)

__all__ = [
    "OrganizationCreateSchema",
    "OrganizationMemberAddSchema",
    "OrganizationMemberResponseSchema",
    "OrganizationMemberUpdateSchema",
    "OrganizationResponseSchema",
    "OrganizationUpdateSchema",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
