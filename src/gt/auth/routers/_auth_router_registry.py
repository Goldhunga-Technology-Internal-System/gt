from ._auth_email_router import create_email_router
from ._auth_onboarding_router import create_onboarding_router
from ._auth_session_router import create_session_router
from ._auth_user_router import create_user_router


def create_auth_router(*, auth):
    """
    Create a router for authentication-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter(prefix="/auth")
    router.include_router(create_user_router(auth=auth), tags=["Authentication Core"])
    router.include_router(
        create_onboarding_router(auth=auth), tags=["Authentication Onboarding"]
    )
    router.include_router(create_email_router(auth=auth), tags=["Authentication Email"])
    router.include_router(
        create_session_router(auth=auth), tags=["Authentication Session"]
    )

    return router
