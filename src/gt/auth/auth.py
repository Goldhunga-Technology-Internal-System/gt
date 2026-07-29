from fastapi import FastAPI, Request
from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from gt.auth.models._auth_user_account_model import create_auth_user_account_model
from gt.auth.models._auth_user_model import create_auth_user_model
from gt.auth.models._auth_user_onboarding_model import (
    TOnboarding,
    create_auth_user_onboarding_model,
)
from gt.auth.models._auth_user_session_model import create_auth_user_session_model
from gt.auth.models._auth_user_tokens_model import create_auth_user_tokens_model
from gt.auth.schemas._auth_onboarding_schemas import AuthOnboardingRegisterSchema
from gt.auth.schemas._auth_schemas import AuthUserRegisterSchema
from gt.auth.settings import AuthSettings
from gt.exceptions._base_exceptions import InvalidException

from .events import event_bus
from .models import AuthUserModel, AuthUserOnboardingModelBase
from .routers import create_auth_router


class Auth[TUser: AuthUserModel]:
    """
    This class is responsible for handling authentication and authorization in the application.
    """

    def __init__(
        self,
        *,
        base: type[DeclarativeBase],
        session_factory: async_sessionmaker[AsyncSession],
        settings: AuthSettings | None = None,
        user_model: type[TUser] | None = None,
        user_onboarding_model: type[TOnboarding] | None = None,
        user_register_schema: type[BaseModel] | None = None,
        onboarding_register_schema: type[AuthOnboardingRegisterSchema] | None = None,
    ):
        """
        Initializes the Auth class.
        """
        self.session_factory = session_factory

        ## setting
        self.settings = settings or AuthSettings()

        ## models
        self.user_model = create_auth_user_model(
            base=base, model=user_model or AuthUserModel
        )
        self.user_onboarding_model = create_auth_user_onboarding_model(
            base=base,
            user_model=self.user_model,
            model=user_onboarding_model or AuthUserOnboardingModelBase,
        )
        self.user_account_model = create_auth_user_account_model(
            base=base, UserModel=self.user_model
        )
        self.user_session_model = create_auth_user_session_model(
            base=base, UserModel=self.user_model
        )
        self.user_tokens_model = create_auth_user_tokens_model(
            base=base, UserModel=self.user_model
        )

        ## schemas
        self.onboarding_register_schema = (
            onboarding_register_schema or AuthOnboardingRegisterSchema
        )
        self.user_register_schema = user_register_schema or AuthUserRegisterSchema
        self.event_bus = event_bus

    def init_app(self, app: FastAPI):
        """
        Initializes the FastAPI application with authentication routes and dependencies.
        """
        self._register_routers(app)
        self._register_exceptions(app)

    ## ----------------------------------------------- Decorators ----------------------------------------------- ##
    def on(self, event_type: type):
        """
        Registers an event handler for a specific event type.

        :param event_type: The type of the event to listen for.
        """

        def decorator(handler):
            self.event_bus.register(event_type, handler)
            return handler

        return decorator

    ## ----------------------------------------------- Dependencies ----------------------------------------------- ##

    async def current_user(self, request: Request) -> TUser | AuthUserModel:
        """
        Dependency function to retrieve the current authenticated user.
        """
        from gt.auth.dependencies._current_user import current_user

        session_uuid = request.cookies.get("session_uuid")
        if not session_uuid:
            raise InvalidException(
                error="Session UUID cookie is missing. Please log in again.",
            )

        return await current_user(
            auth=self,
            session_uuid=session_uuid,
        )

    ## ----------------------------------------------- Private Methods ----------------------------------------------- ##

    def _register_routers(self, app: FastAPI):
        """
        Registers authentication-related routers to the FastAPI application.
        """
        routers = create_auth_router(auth=self)
        app.include_router(routers)

    def _register_exceptions(self, app: FastAPI):
        """
        Registers custom exception handlers to the FastAPI application.
        """
        from gt.exceptions import add_exceptions_handler

        add_exceptions_handler(app)
