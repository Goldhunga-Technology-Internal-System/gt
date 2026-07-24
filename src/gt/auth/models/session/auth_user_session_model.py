from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from sqlalchemy import ForeignKey, String, DateTime
from datetime import datetime

Base = declarative_base()


def create_auth_user_session_model(UserModel):
    """
    Factory function to create the AuthUserSessionModel class.
    """

    class AuthUserSessionModel(Base):
        """
        AuthUserSessionModel is a model that represents a user session in the authentication system.
        """

        __tablename__ = "sys_auth_user_sessions"

        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )
        expires_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), nullable=False
        )

        ## Optional fields
        device: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        ip_address: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        browser: Mapped[str | None] = mapped_column(
            String(255), nullable=True, default=None
        )
        revoked_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True, default=None
        )

        def __repr__(self) -> str:
            return f"<AuthUserSessionModel(user_id={self.user_id}, session_token={self.session_token}, expires_at={self.expires_at})>"

        def __str__(self) -> str:
            return f"AuthUserSessionModel(user_id={self.user_id},  expires_at={self.expires_at})"

    return AuthUserSessionModel()
