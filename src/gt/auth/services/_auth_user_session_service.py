from datetime import UTC, datetime, timedelta
from typing import Any, cast

from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.repositories._auth_user_session_repository import TSession
from gt.exceptions import DomainException

from ..repositories import AuthUserSessionRepository


class AuthUserSessionService[TSession]:
    """Service for managing auth user session operations."""

    def __init__(
        self, repository: AuthUserSessionRepository[TSession], model: type[TSession]
    ):
        """Initialize the service with a repository and model.

        Args:
            repository: The AuthUserSessionRepository instance.
            model: The AuthUserSessionModel class.
        """
        self._repository = repository
        self._model = model

    async def create_session(
        self,
        user_id: int,
        expire_minutes: int,
        device: str,
        ip_address: str,
        browser: str,
    ) -> TSession:
        """Create a new user session.

        Args:
            session_record: The session model instance to create.

        Returns:
            The created session instance.

        Raises:
            ConflictException: If a session with the same uuid already exists.
            DomainException: On unexpected failures.
        """
        try:
            model_cls = cast("type[Any]", self._model)
            session = model_cls(
                user_id=user_id,
                expires_at=datetime.now(UTC) + timedelta(minutes=expire_minutes),
                device=device,
                ip_address=ip_address,
                browser=browser,
            )
            return await self._repository.add(session)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to create session.",
                internal_details=str(e),
            ) from e

    async def get_session_by(self, **kwargs) -> TSession | None:
        """Retrieve a session by filter criteria.

        Args:
            **kwargs: Filter keyword arguments.

        Returns:
            The matching session instance or None.

        Raises:
            DomainException: On unexpected failures.
        """
        try:
            return await self._repository.get_by(**kwargs)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to retrieve session.",
                internal_details=str(e),
            ) from e


def get_auth_user_session_service(
    session: AsyncSession, model: type[TSession]
) -> AuthUserSessionService:
    """Factory function to create an AuthUserSessionService instance.

    Args:
        session: Async SQLAlchemy session.
        model: The AuthUserSessionModel class.

    Returns:
        A configured AuthUserSessionService.
    """
    repository = AuthUserSessionRepository(session=session, model=model)
    return AuthUserSessionService(repository=repository, model=model)
