from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from gt.auth.repositories._auth_user_account_repository import TAccount
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.settings import AuthSettings

from ..models import AuthUserModel, AuthUserOnboardingModel
from ._auth_user_router import create_user_router


def create_auth_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    settings: AuthSettings,
    user_model: type[AuthUserModel],
    user_onboarding_model: type[AuthUserOnboardingModel],
    user_account_model: type[TAccount],
    user_session_model: type[TSession],
    user_tokens_model: type,
    onboarding_register_schema: type[BaseModel],
    user_register_schema: type[BaseModel],
):
    """
    Create a router for authentication-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter(prefix="/auth", tags=["Authentication"])
    router.include_router(
        create_user_router(
            session_factory=session_factory,
            settings=settings,
            user_model=user_model,
            user_account_model=user_account_model,
            user_session_model=user_session_model,
            user_register_schema=user_register_schema,
        )
    )

    return router
