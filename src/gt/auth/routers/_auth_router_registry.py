from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from gt.auth.models._auth_user_model import TUser
from gt.auth.models._auth_user_onboarding_model import TOnboarding
from gt.auth.repositories._auth_user_account_repository import TAccount
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.repositories._auth_user_tokens_repository import TToken
from gt.auth.routers._auth_onboarding_router import create_onboarding_router
from gt.auth.schemas._auth_onboarding_schemas import AuthOnboardingRegisterSchema
from gt.auth.settings import AuthSettings

from ._auth_user_router import create_user_router


def create_auth_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    settings: AuthSettings,
    user_model: type[TUser],
    user_onboarding_model: type[TOnboarding],
    user_account_model: type[TAccount],
    user_session_model: type[TSession],
    user_tokens_model: type[TToken],
    onboarding_register_schema: type[AuthOnboardingRegisterSchema],
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
            user_tokens_model=user_tokens_model,
            user_register_schema=user_register_schema,
        )
    )
    router.include_router(
        create_onboarding_router(
            session_factory=session_factory,
            user_onboarding_model=user_onboarding_model,
            user_onboarding_register_schema=onboarding_register_schema,
        )
    )

    return router
