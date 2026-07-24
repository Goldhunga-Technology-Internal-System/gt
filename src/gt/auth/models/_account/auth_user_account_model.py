import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


def create_auth_user_account_model(base, UserModel):
    """
    Factory function to create the AuthUserAccountModel class.

    This function defines the AuthUserAccountModel class, which represents a user account in the authentication system.
    It is defined within this function to avoid circular import issues.

    Returns:
        AuthUserAccountModel: The AuthUserAccountModel class.
    """

    class AuthUserAccoutModel(base):
        """
        AuthUserAccountModel is a model that represents a user account in the authentication system.

        This model needs to be inherited from the BaseModel class to be used with SQLModel. It contains the following fields:
            -id : The primary key of the user account model.
            -uuid : A unique identifier for the user account model, generated using the uuid4 function.

        """

        __tablename__ = "auth_user_accounts"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        uuid: Mapped[str] = mapped_column(
            unique=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
        )
        type: Mapped[str] = mapped_column(String(255), nullable=False)
        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )

        ## Optional fields
        hashed_password: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        provider: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        last_password_updated_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True, default=None
        )

        def __repr__(self) -> str:
            return f"<AuthUserAccoutModel(id={self.id}, uuid={self.uuid}, type={self.type}, user_id={self.user_id})>"

        def __str__(self) -> str:
            return f"AuthUserAccoutModel(id={self.id}, uuid={self.uuid}, type={self.type}, user_id={self.user_id})"

    return AuthUserAccoutModel()
