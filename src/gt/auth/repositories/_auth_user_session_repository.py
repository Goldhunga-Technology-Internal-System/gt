from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gt.exceptions import CreateException

TSession = TypeVar("TSession")


class AuthUserSessionRepository[TSession]:
    """Repository for managing auth user session persistence."""

    def __init__(self, session: AsyncSession, model: type[TSession]):
        """Initialize the repository with a database session and model.

        Args:
            session: Async SQLAlchemy session.
            model: The AuthUserSessionModel class.
        """
        self.session = session
        self.model = model

    async def add(self, session_record: TSession) -> TSession:
        """Add a new session record to the database.

        Args:
            session_record: The session model instance to persist.

        Returns:
            The persisted session instance.
        """
        try:
            self.session.add(session_record)
            await self.session.flush()
            await self.session.refresh(session_record)
            return session_record
        except Exception as e:
            raise CreateException(
                error="Failed to add session to the database.",
                internal_details=str(e),
            ) from e

    async def get_by(self, **kwargs) -> TSession | None:
        """Retrieve a session record by arbitrary filter criteria.

        Args:
            **kwargs: Filter keyword arguments passed to filter_by.

        Returns:
            The matching session instance or None.
        """
        try:
            stmt = select(self.model).filter_by(**kwargs)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise CreateException(
                error="Failed to retrieve session from the database.",
                internal_details=str(e),
            ) from e
