import uuid

from sqlalchemy.orm import Mapped, mapped_column


class AuthUserOnboardingModel:
    """
    AuthUserOnboardingModel is a model that represents the onboarding process of a user in the authentication system.

    This model needs to be inherited from the BaseModel class to be used with SQLModel. It contains the following fields:
        -id : The primary key of the user onboarding model.
        -uuid : A unique identifier for the user onboarding model, generated using the uuid4 function.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    uuid: Mapped[str] = mapped_column(
        unique=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
    )
