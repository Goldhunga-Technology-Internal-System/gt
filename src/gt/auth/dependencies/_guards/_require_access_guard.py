from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.policies import UserPolicies
from gt.exceptions._base_exceptions import UnauthorizedException


def require_access(
    *,
    authenticated: bool = True,
    email_verified: bool = False,
    onboarded: bool = False,
    auth,
):
    """
    Build a reusable access dependency for router/endpoint-level authorization.
    """
    needs_user = authenticated or email_verified or onboarded

    async def dependency(
        request: Request,
        session: AsyncSession = Depends(auth.get_db_session),
    ):

        session_uuid = request.cookies.get("session_uuid")
        user = (
            await auth.current_user(request=request, session=session)
            if session_uuid
            else None
        )

        if needs_user and user is None:
            raise UnauthorizedException(
                error="Authentication required",
                errors={"code": "UNAUTHENTICATED"},
            )

        if email_verified and user is not None:
            UserPolicies.require_email_verified(user)

        if onboarded and user is not None:
            UserPolicies.require_onboarding(user)

        return user

    return dependency
