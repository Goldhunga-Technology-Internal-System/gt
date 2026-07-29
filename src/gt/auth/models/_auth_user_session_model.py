import uuid
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class AuthUserSessionModelBase(MappedAsDataclass):
    """
    Base class for the AuthUserSessionModel.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)

    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    uuid: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
    )

    device: Mapped[str | None] = mapped_column(String(255), nullable=True, default=None)
    ip_address: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    browser: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, init=False
    )

    @property
    def is_expired(self) -> bool:
        """Check if the session has expired based on the current time."""
        return datetime.now(UTC) >= self.expires_at

    @property
    def is_active(self) -> bool:
        """Check if the session is active (not expired and not revoked)."""
        return not self.is_expired and self.revoked_at is None

    def revoke(self) -> None:
        """Mark the session as revoked by setting the revoked_at timestamp."""
        self.revoked_at = datetime.now(UTC)


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

    class AuthUserSessionModel(AuthUserSessionModelBase, base):
        """Represents an active user session in the application."""

        __tablename__ = "auth_user_sessions"

        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )

        def __repr__(self) -> str:
            """Provide representation details for debugging."""
            return f"<AuthUserSessionModel(id={self.id}, uuid={self.uuid}, user_id={self.user_id}, expires_at={self.expires_at})>"

        def __str__(self) -> str:
            """Provide string format of the class."""
            return f"AuthUserSessionModel(id={self.id}, uuid={self.uuid}, user_id={self.user_id}, expires_at={self.expires_at})"

    return AuthUserSessionModel
