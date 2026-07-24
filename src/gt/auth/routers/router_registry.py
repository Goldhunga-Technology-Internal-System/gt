from fastapi import APIRouter

from .auth_user_router import router as auth_user_router

router = APIRouter(
    prefix="/auth",
)


router.include_router(auth_user_router)


def register_auth_routers(app):
    """
    Register the authentication routers with the FastAPI application.
    """
    app.include_router(router)
