from ._auth_onboarding_router import create_onboarding_router
from ._auth_user_router import create_user_router


def create_auth_router(*, auth):
    """
    Create a router for authentication-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.include_router(create_user_router(auth=auth))
    router.include_router(create_onboarding_router(auth=auth))

    return router
