from ._organization_member_repository import (
    OrganizationMemberRepository,
    TOrganizationMember,
)
from ._organization_repository import OrganizationRepository, TOrganization

__all__ = [
    "OrganizationMemberRepository",
    "OrganizationRepository",
    "TOrganization",
    "TOrganizationMember",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
