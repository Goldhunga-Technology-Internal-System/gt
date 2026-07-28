from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from gt.auth.models import AuthUserModel
from gt.auth.services import AuthUserService, get_auth_user_service

from ..uow import AuthUOW


def create_user_router(
    session_factory: async_sessionmaker[AsyncSession],
    model: type[AuthUserModel],
    user_register_schema: type[BaseModel],
):
    """
    Create a router for user-related operations.
    """

    from fastapi import APIRouter

    router = APIRouter()

    @router.post("/register")
    async def register_user(body: user_register_schema):  # type: ignore
        """
        Endpoint to register a new user.
        """
        async with session_factory() as session:
            user_service: AuthUserService = get_auth_user_service(session, model)

            async with AuthUOW(session):
                user = model(**body.model_dump())
                _ = await user_service.create_user(user)

        return {"message": "Successfully registered user"}

    return router
