import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


def create_auth_user_session_model(base: Any, UserModel: Any) -> Any:
    """Factory function to dynamically create the AuthUserSessionModel class.

    Injects the application-specific base and User model to establish
    relationships and avoid circular dependencies.

    Args:
        base: The declarative base class (SQLAlchemy or SQLModel).
        UserModel: The concrete user model class.

    Returns:
        The constructed AuthUserSessionModel class.
    """

    class AuthUserSessionModel(base):
        """Represents an active user session in the application."""

        __tablename__ = "auth_user_sessions"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )
        expires_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), nullable=False
        )
        uuid: Mapped[str] = mapped_column(
            unique=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
        )

        device: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        ip_address: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        browser: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        revoked_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True, default=None
        )

        def __repr__(self) -> str:
            """Provide representation details for debugging."""
            return f"<AuthUserSessionModel(id={self.id}, uuid={self.uuid}, user_id={self.user_id}, expires_at={self.expires_at})>"

        def __str__(self) -> str:
            """Provide string format of the class."""
            return f"AuthUserSessionModel(id={self.id}, uuid={self.uuid}, user_id={self.user_id}, expires_at={self.expires_at})"

    return AuthUserSessionModel
