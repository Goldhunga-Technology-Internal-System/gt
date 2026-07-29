import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class AuthUserTokensModelBase(MappedAsDataclass):
    """Base class for the AuthUserTokensModel."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    user_id: Mapped[int] = mapped_column(nullable=False, index=True)

    type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    token_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    uuid: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
    )

    used_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, init=False
    )


def create_auth_user_tokens_model(base: Any, UserModel: Any) -> Any:
    """Factory function to dynamically create the AuthUserTokensModel class.

    Injects the application-specific base and User model to establish
    relationships and avoid circular dependencies.

    Args:
        base: The declarative base class (SQLAlchemy or SQLModel).
        UserModel: The concrete user model class.

    Returns:
        The constructed AuthUserTokensModel class.
    """

    class AuthUserTokensModel(AuthUserTokensModelBase, base):
        """Represents a token issued for a user (e.g. password resets, verification)."""

        __tablename__ = "auth_user_tokens"

        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )

        def __repr__(self) -> str:
            """Provide representation details for debugging."""
            return f"<AuthUserTokensModel(user_id={self.user_id}, type={self.type}, token_hash={self.token_hash}, expires_at={self.expires_at}, used_at={self.used_at})>"

        def __str__(self) -> str:
            """Provide string format of the class."""
            return f"AuthUserTokensModel(user_id={self.user_id}, type={self.type}, expires_at={self.expires_at}, used_at={self.used_at})"

    return AuthUserTokensModel
