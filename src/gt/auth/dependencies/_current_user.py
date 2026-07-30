"""
Current user dependency for FastAPI routes. This module provides a function to retrieve the current authenticated user based on the provided session uuid.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.auth import Auth
from gt.auth.models._auth_user_model import AuthUserModel
from gt.auth.services._auth_user_service import get_auth_user_service
from gt.exceptions._base_exceptions import InvalidException


async def current_user(
    *,
    auth: Auth,
    session: AsyncSession,
    session_uuid: str,
) -> AuthUserModel:
    """
    Dependency function to retrieve the current authenticated user.

    Returns:
        The current authenticated user object if the session is valid, otherwise raises an HTTPException.
    """

    user_model = auth.user_model
    account_model = auth.user_account_model
    session_model = auth.user_session_model
    token_model = auth.user_tokens_model

    # Implementation to retrieve the current user based on session uuid
    user_service = get_auth_user_service(
        session=session,
        user_model=user_model,
        account_model=account_model,
        session_model=session_model,
        token_model=token_model,
    )

    user_session = await user_service._session_service.get_session_by(uuid=session_uuid)

    if not user_session or not user_session.is_active:
        raise InvalidException(
            error="Invalid or expired session.",
        )

    user = await user_service.get_user_by(id=user_session.user_id)

    if not user or not user.is_active():
        raise InvalidException(
            error="User is inactive or does not exist.",
        )

    return user
