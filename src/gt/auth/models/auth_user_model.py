import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column


class AuthUserModel:
    """Represents a user in the authentication system.

    This model serves as an abstract base for user information, intended to be
    inherited by SQLModel / SQLAlchemy models in the application.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    uuid: Mapped[str] = mapped_column(
        unique=True,
        nullable=False,
        default_factory=lambda: str(uuid.uuid4()),
        init=False,
    )
    email: Mapped[str] = mapped_column(
        unique=True, nullable=False, index=True, init=False
    )
    avatar_bg: Mapped[str] = mapped_column(String(255), nullable=False, init=False)
    avatar: Mapped[str] = mapped_column(String(255), nullable=True, init=False)
    is_onboarded: Mapped[bool] = mapped_column(
        Boolean, nullable=False, index=True, init=False, default=False
    )
    status: Mapped[str] = mapped_column(
        String(255), nullable=False, default="active", index=True, init=False
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=False, init=False)
    email_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
