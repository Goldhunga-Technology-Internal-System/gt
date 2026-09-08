from ._organization_member_service import (
    OrganizationMemberService,
    get_organization_member_service,
)
from ._organization_service import OrganizationService, get_organization_service

__all__ = [
    "OrganizationMemberService",
    "OrganizationService",
    "get_organization_member_service",
    "get_organization_service",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
