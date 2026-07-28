from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from ..models import AuthUserModel, AuthUserOnboardingModel
from .auth_user_router import create_user_router


def create_auth_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    user_model: type[AuthUserModel],
    user_register_schema: type[BaseModel],
    user_onboarding_model: type[AuthUserOnboardingModel],
    onboarding_register_schema: type[BaseModel],
):
    """
    Create a router for authentication-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.include_router(
        create_user_router(session_factory, user_model, user_register_schema)
    )

    return router
