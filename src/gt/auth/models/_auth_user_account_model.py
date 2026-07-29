import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class AuthUserAccountModelBase(MappedAsDataclass):
    """Base class for the AuthUserAccountModel."""

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False, kw_only=True
    )
    type: Mapped[str] = mapped_column(String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)

    uuid: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
    )

    hashed_password: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    provider: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None
    )
    last_password_updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, init=False
    )


def create_auth_user_account_model(base: Any, UserModel: Any) -> Any:
    """Factory function to dynamically create the AuthUserAccountModel class.

    Injects the application-specific base and User model to establish
    relationships and avoid circular dependencies.

    Args:
        base: The declarative base class (SQLAlchemy or SQLModel).
        UserModel: The concrete user model class.

    Returns:
        The constructed AuthUserAccountModel class.
    """

    class AuthUserAccountModel(AuthUserAccountModelBase, base):
        """Represents a user credentials account (e.g., passwords or OAuth providers)."""

        __tablename__ = "auth_user_accounts"

        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )

        def __repr__(self) -> str:
            """Provide representation details for debugging."""
            return f"<AuthUserAccountModel(id={self.id}, uuid={self.uuid}, type={self.type}, user_id={self.user_id})>"

        def __str__(self) -> str:
            """Provide string format of the class."""
            return f"AuthUserAccountModel(id={self.id}, uuid={self.uuid}, type={self.type}, user_id={self.user_id})"

    return AuthUserAccountModel
