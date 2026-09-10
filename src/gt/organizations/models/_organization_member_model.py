import uuid
from typing import ClassVar, TypeVar, cast

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column

from gt.auth.models._auth_user_model import TUser
from gt.organizations.models._organization_model import TOrganization


class OrganizationMemberModelBase(MappedAsDataclass):
    """Represents the membership of a user in an organization.

    This model serves as an abstract base for membership details, intended to be
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
    user_id: Mapped[int] = mapped_column(
        kw_only=True, nullable=False
    )  # This will be defined in the factory function
    organization_id: Mapped[int] = mapped_column(
        kw_only=True, nullable=False
    )  # This will be defined in the factory function
    status: Mapped[str] = mapped_column(
        String(255), nullable=False, default="active", index=True, kw_only=True
    )
    role: Mapped[str] = mapped_column(
        String(255), nullable=False, default="member", index=True, kw_only=True
    )

    def is_active(self) -> bool:
        """Check if the membership is active.

        Returns:
            bool: True if the membership's status is 'active', False otherwise.
        """
        return self.status == "active"


TOrganizationMember = TypeVar("TOrganizationMember", bound=OrganizationMemberModelBase)


def create_organization_member_model(
    base: type,
    user_model: type[TUser],
    organization_model: type[TOrganization],
    model: type[TOrganizationMember] = OrganizationMemberModelBase,
) -> type[TOrganizationMember]:
    """Create the concrete organization member model.

    Injects the application-specific base, User and Organization models to establish
    relationships and avoid circular dependencies.

    If the model does not define ``__tablename__``, it defaults to
    ``"sys_organization_members"``.

    Args:
        base: The declarative base class (SQLAlchemy or SQLModel).
        user_model: The concrete user model class.
        organization_model: The concrete organization model class.
        model: The organization member model base to construct.

    Returns:
        The constructed OrganizationMemberModel class.
    """

    attrs: dict[str, object] = {}

    if "__tablename__" not in model.__dict__:
        attrs["__tablename__"] = "sys_organization_members"

    attrs["user_id"] = mapped_column(
        ForeignKey(f"{user_model.__tablename__}.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    attrs["organization_id"] = mapped_column(
        ForeignKey(f"{organization_model.__tablename__}.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    cls = type(model.__name__, (base, model), attrs)
    return cast(type[TOrganizationMember], cls)
