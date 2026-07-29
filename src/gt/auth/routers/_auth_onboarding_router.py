from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from gt.auth.models._auth_user_model import TUser
from gt.auth.models._auth_user_onboarding_model import TOnboarding
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.schemas._auth_onboarding_schemas import AuthOnboardingRegisterSchema
from gt.auth.services._auth_user_onboarding_service import (
    get_auth_user_onboarding_service,
)
from gt.auth.services._auth_user_session_service import (
    get_auth_user_session_service,
)
from gt.response import cr

from ..uow import AuthUOW


def create_onboarding_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    user_model: type[TUser],
    user_session_model: type[TSession],
    user_onboarding_model: type[TOnboarding],
    user_onboarding_register_schema: type[AuthOnboardingRegisterSchema],
):
    """
    Create a router for user onboarding operations.
    """

    from fastapi import APIRouter

    router = APIRouter()

    @router.post("/onboarding")
    async def register_onboarding(
        request: Request,
        body: user_onboarding_register_schema,  # type: ignore
    ):
        """
        Endpoint to register a new user onboarding.
        """
        session_uuid = request.cookies.get("session_uuid")
        if not session_uuid:
            return cr.error(
                error="No active session found.",
                status_code=HTTP_400_BAD_REQUEST,
            )

        async with session_factory() as session:
            session_service = get_auth_user_session_service(
                session=session, model=user_session_model
            )

            async with AuthUOW(session):
                user_session = await session_service.get_session_by(uuid=session_uuid)
                if not user_session or not user_session.is_active:
                    return cr.error(
                        error="Invalid or expired session.",
                        status_code=HTTP_400_BAD_REQUEST,
                    )

                onboarding_service = get_auth_user_onboarding_service(
                    session=session,
                    model=user_onboarding_model,
                )
                await onboarding_service.add_onboarding(
                    user_id=user_session.user_id,
                    theme=body.theme,
                    referral_source=body.referral_source,
                )

        return cr.success(
            message="Onboarding completed successfully.",
            status_code=HTTP_201_CREATED,
        )

    return router
