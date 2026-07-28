import uuid

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
