"""
Current user dependency for FastAPI routes. This module provides a function to retrieve the current authenticated user based on the provided session uuid.
"""

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from gt.auth.models._auth_user_model import AuthUserModel
from gt.auth.repositories._auth_user_account_repository import TAccount
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.repositories._auth_user_tokens_repository import TToken
from gt.auth.services._auth_user_service import AuthUserService, get_auth_user_service
from gt.exceptions._base_exceptions import InvalidException


async def current_user(
    session_uuid: str,
    session_factory: async_sessionmaker[AsyncSession],
    user_model: type[AuthUserModel],
    account_model: type[TAccount],
    session_model: type[TSession],
    token_model: type[TToken],
) -> AuthUserModel:
    """
    Dependency function to retrieve the current authenticated user.

    Returns:
        The current authenticated user object if the session is valid, otherwise raises an HTTPException.
    """
    # Implementation to retrieve the current user based on session uuid
    async with session_factory() as session:
        user_service: AuthUserService = get_auth_user_service(
            session=session,
            user_model=user_model,
            account_model=account_model,
            session_model=session_model,
            token_model=token_model,
        )

        session = await user_service._session_service.get_session_by(uuid=session_uuid)

        if not session or not session.is_active:
            raise InvalidException(
                error="Invalid or expired session.",
            )

        user = await user_service.get_user_by(id=session.user_id)

        if not user or not user.is_active():
            raise InvalidException(
                error="User is inactive or does not exist.",
            )

        return user
