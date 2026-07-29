import uuid
from typing import ClassVar, TypeVar, cast

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from gt.auth.models._auth_user_model import TUser


class AuthUserOnboardingModelBase(MappedAsDataclass):
    """Represents the onboarding state/process of a user.

    This model serves as an abstract base for onboarding details, intended to be
    inherited by SQLModel / SQLAlchemy models in the application.
    """

    __abstract__ = True
    __tablename__: ClassVar[str]

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
    theme: Mapped[str] = mapped_column(nullable=False, default="light", kw_only=True)
    referral_source: Mapped[str | None] = mapped_column(
        nullable=True, default=None, kw_only=True
    )
    user_id: Mapped[int]  # This will be defined in the factory function


TOnboarding = TypeVar("TOnboarding", bound=AuthUserOnboardingModelBase)


def create_auth_user_onboarding_model(
    base: type,
    user_model: type[TUser],
    model: type[TOnboarding] = AuthUserOnboardingModelBase,
) -> type[TOnboarding]:
    """Factory function to dynamically create the AuthUserOnboardingModel class."""

    attrs: dict[str, object] = {}

    if "__tablename__" not in model.__dict__:
        attrs["__tablename__"] = "auth_user_onboardings"

    attrs["user_id"] = mapped_column(
        ForeignKey(f"{user_model.__tablename__}.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # one onboarding row per user
        index=True,
    )

    cls = type(model.__name__, (base, model), attrs)
    return cast(type[TOnboarding], cls)
