import uuid

from sqlalchemy.orm import Mapped, mapped_column


class AuthUserOnboardingModel:
    """Represents the onboarding state/process of a user.

    This model serves as an abstract base for onboarding details, intended to be
    inherited by SQLModel / SQLAlchemy models in the application.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        unique=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
    )
