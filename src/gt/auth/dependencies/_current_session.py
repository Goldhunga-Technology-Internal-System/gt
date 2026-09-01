"""
Current session dependency function for retrieving the authenticated session.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.auth import Auth
from gt.auth.services._auth_user_service import get_auth_user_service
from gt.exceptions._base_exceptions import InvalidException


async def current_session(
    *,
    auth: Auth,
    session: AsyncSession,
    session_uuid: str,
):
    """
    Dependency function to retrieve the current authenticated session.
    """
    user_model = auth.user_model
    account_model = auth.user_account_model
    session_model = auth.user_session_model
    token_model = auth.user_tokens_model

    # Implementation to retrieve the current session based on session uuid
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
            error="Invalid or expired session.", errors={"code": "SESSION_INVALID"}
        )

    return user_session
