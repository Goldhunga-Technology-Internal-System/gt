import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class AuthUserModel(MappedAsDataclass):
    """Represents a user in the authentication system.

    This model serves as an abstract base for user information, intended to be
    inherited by SQLModel / SQLAlchemy models in the application.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, init=False, kw_only=True
    )
    uuid: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
        kw_only=True,
    )
    email: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True, kw_only=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, kw_only=True)
    avatar_bg: Mapped[str] = mapped_column(String(255), nullable=False, kw_only=True)
    is_onboarded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, index=True, default=False, kw_only=True
    )
    status: Mapped[str] = mapped_column(
        String(255), nullable=False, default="active", index=True, kw_only=True
    )
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, init=False, kw_only=True
    )
    avatar: Mapped[str | None] = mapped_column(
        String(255), nullable=True, default=None, kw_only=True
    )
