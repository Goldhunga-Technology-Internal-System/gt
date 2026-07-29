from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from gt.auth.models._auth_user_onboarding_model import TOnboarding
from gt.auth.schemas._auth_onboarding_schemas import AuthOnboardingRegisterSchema


def create_onboarding_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    user_onboarding_model: type[TOnboarding],
    user_onboarding_register_schema: type[AuthOnboardingRegisterSchema],
):
    """
    Create a router for user onboarding operations.
    """

    from fastapi import APIRouter, Request

    router = APIRouter()

    @router.post("/onboarding")
    async def register_onboarding(
        request: Request,
        body: user_onboarding_register_schema,  # type: ignore
    ):
        """
        Endpoint to register a new user onboarding.
        """

    return router
