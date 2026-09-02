from typing import Literal

from fastapi import APIRouter
from fastapi.param_functions import Path
from fastapi.requests import Request


def create_oauth_router(*, auth):
    """
    Create a router for OAuth-related operations.
    """

    from gt.auth.services._auth_oauth_service import get_auth_oauth_service
    from gt.auth.uow._auth_uow import AuthUOW

    session_factory = auth.session_factory
    # user_model = auth.user_model
    # user_account_model = auth.user_account_model
    # user_session_model = auth.user_session_model
    settings = auth.settings

    router = APIRouter(prefix="/oauth")

    @router.get("/login/{provider}")
    async def oauth_login(
        request: Request,
        provider: Literal["google"] = Path(..., description="OAuth provider name"),
    ):
        """
        Endpoint to initiate the OAuth login process for a given provider.
        """

        async with session_factory() as session:
            oauth_service = get_auth_oauth_service(
                settings=settings,
                provider=provider,
            )

            async with AuthUOW(session):
                return await oauth_service.authorize_redirect(request=request)

    return router
