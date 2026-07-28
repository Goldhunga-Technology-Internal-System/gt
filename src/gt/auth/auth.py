from fastapi import FastAPI
from pydantic.main import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .events import event_bus
from .models import AuthUserModel, AuthUserOnboardingModel
from .routers import create_auth_router


class Auth:
    """
    This class is responsible for handling authentication and authorization in the application.
    """

    def __init__(
        self,
        *,
        session_factory: async_sessionmaker[AsyncSession],
        user_model: type[AuthUserModel],
        user_onboarding_model: type[AuthUserOnboardingModel],
        user_register_schema: type[BaseModel],
        onboarding_register_schema: type[BaseModel],
    ):
        """
        Initializes the Auth class.
        """
        self.session_factory = session_factory
        self.user_model = user_model
        self.user_register_schema = user_register_schema
        self.user_onboarding_model = user_onboarding_model
        self.onboarding_register_schema = onboarding_register_schema
        self.event_bus = event_bus

    def init_app(self, app: FastAPI):
        """
        Initializes the FastAPI application with authentication routes and dependencies.
        """
        self._register_routers(app)
        self._register_exceptions(app)

    def on(self, event_type: type):
        """
        Registers an event handler for a specific event type.

        :param event_type: The type of the event to listen for.
        """

        def decorator(handler):
            self.event_bus.register(event_type, handler)
            return handler

        return decorator

    def _register_routers(self, app: FastAPI):
        """
        Registers authentication-related routers to the FastAPI application.
        """
        routers = create_auth_router(
            session_factory=self.session_factory,
            user_model=self.user_model,
            user_register_schema=self.user_register_schema,
            user_onboarding_model=self.user_onboarding_model,
            onboarding_register_schema=self.onboarding_register_schema,
        )
        app.include_router(routers)

    def _register_exceptions(self, app: FastAPI):
        """
        Registers custom exception handlers to the FastAPI application.
        """
        from gt.exceptions import add_exceptions_handler

        add_exceptions_handler(app)
