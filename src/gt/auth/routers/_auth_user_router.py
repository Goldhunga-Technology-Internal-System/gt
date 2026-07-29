from fastapi.requests import Request
from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from gt.auth.models import AuthUserModel
from gt.auth.repositories._auth_user_account_repository import TAccount
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.services import AuthUserService, get_auth_user_service
from gt.auth.settings import AuthSettings
from gt.ip import IPService
from gt.response import cr
from gt.response._response import get_cookie_response

from ..uow import AuthUOW


def create_user_router(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    settings: AuthSettings,
    user_model: type[AuthUserModel],
    user_account_model: type[TAccount],
    user_session_model: type[TSession],
    user_register_schema: type[BaseModel],
):
    """
    Create a router for user-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter()

    @router.post("/register")
    async def register_user(request: Request, body: user_register_schema):  # type: ignore
        """
        Endpoint to register a new user.
        """
        ip_context = IPService.get_ip_context(request)
        async with session_factory() as session:
            user_service: AuthUserService = get_auth_user_service(
                session=session,
                user_model=user_model,
                account_model=user_account_model,
                session_model=user_session_model,
            )

            async with AuthUOW(session):
                user = user_model(**body.model_dump(exclude={"password"}))
                _, user_session = await user_service.create_user(
                    user,
                    password=body.password,
                    ip_address=ip_context.ip_address,
                    device=ip_context.device,
                    browser=ip_context.browser,
                    session_expire_minutes=10,
                )

        response = cr.success(
            message="User registered successfully.",
            data={"session_uuid": user_session.uuid},
        )
        return get_cookie_response(
            response=response,
            key="session_uuid",
            value=str(user_session.uuid),
            max_age=settings.session_expiration_minutes,
            httponly=settings.cookie_httponly,
            secure=settings.cookie_secure,
            samesite=settings.cookie_samesite,
            domain=settings.cookie_domain,
            path=settings.cookie_path,
        )

    return router
