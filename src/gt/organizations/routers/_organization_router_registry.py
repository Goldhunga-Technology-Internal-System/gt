from ._organization_member_router import create_organization_member_router
from ._organization_router import create_organization_router


def create_organizations_router(*, organizations):
    """
    Create a router for organization-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter(prefix="/organizations")
    router.include_router(
        create_organization_router(organizations=organizations),
        tags=["Organizations"],
    )
    router.include_router(
        create_organization_member_router(organizations=organizations),
        tags=["Organization Members"],
    )

    return router
