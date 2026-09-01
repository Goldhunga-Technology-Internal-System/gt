from fastapi.requests import Request

from gt.auth.schemas._auth_session_schema import CurrentSessionResponseSchema
from gt.response import cr


def create_session_router(*, auth):
    """
    Create a router for session-related operations.
    """
    session_factory = auth.session_factory
    user_session_model = auth.user_session_model

    from fastapi import APIRouter

    from gt.auth.services._auth_user_session_service import (
        AuthUserSessionService,
        get_auth_user_session_service,
    )

    router = APIRouter(prefix="/session")

    @router.get("/current")
    async def current_session(request: Request):
        """
        Endpoint to log out a user by invalidating their session.
        """
        session_uuid = request.cookies.get("session_uuid")
        if not session_uuid:
            return cr.error(
                error="No session found.",
                errors={"code": "SESSION_NOT_FOUND"},
            )

        async with session_factory() as session:
            user_session_service: AuthUserSessionService = (
                get_auth_user_session_service(
                    session=session,
                    model=user_session_model,
                )
            )

            # Invalidate the user's session here (implementation depends on your session management)
            current = await user_session_service.get_session_by(uuid=session_uuid)

            if not current or not current.is_active:
                return cr.error(
                    error="Invalid or expired session.",
                    errors={"code": "SESSION_INVALID"},
                )

        return cr.success(
            data=CurrentSessionResponseSchema.model_validate(
                current,
            ).model_dump(),
            message="Successfully retrieved current session.",
        )

    return router
