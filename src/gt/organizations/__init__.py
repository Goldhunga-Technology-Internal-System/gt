from .models import (
    OrganizationMemberModelBase,
    OrganizationModel,
    create_organization_member_model,
    create_organization_model,
    generate_slug,
)
from .organizations import Organizations
from .repositories import (
    OrganizationMemberRepository,
    OrganizationRepository,
)
from .schemas import (
    OrganizationCreateSchema,
    OrganizationMemberAddSchema,
    OrganizationMemberResponseSchema,
    OrganizationMemberUpdateSchema,
    OrganizationResponseSchema,
    OrganizationUpdateSchema,
)
from .services import (
    OrganizationMemberService,
    OrganizationService,
    get_organization_member_service,
    get_organization_service,
)

__all__ = [
    "OrganizationCreateSchema",
    "OrganizationMemberAddSchema",
    "OrganizationMemberModelBase",
    "OrganizationMemberRepository",
    "OrganizationMemberResponseSchema",
    "OrganizationMemberService",
    "OrganizationMemberUpdateSchema",
    "OrganizationModel",
    "OrganizationRepository",
    "OrganizationResponseSchema",
    "OrganizationService",
    "OrganizationUpdateSchema",
    "Organizations",
    "create_organization_member_model",
    "create_organization_model",
    "generate_slug",
    "get_organization_member_service",
    "get_organization_service",
]


def __getattr__(name: str):
    if name in __all__:
        return globals()[name]
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
