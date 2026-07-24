from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


def create_auth_user_tokens_model(base, UserModel):
    """
    Factory function to create the AuthUserTokensModel class.
    """

    class AuthUserTokensModel(base):
        """
        AuthUserTokensModel is a model that represents a user token in the authentication system.
        """

        __tablename__ = "auth_user_tokens"

        user_id: Mapped[int] = mapped_column(
            ForeignKey(f"{UserModel.__tablename__}.id", ondelete="cascade"),
            nullable=False,
            index=True,
        )
        type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
        token_hash: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
        expires_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), nullable=False, index=True
        )

        ## Optional fields
        used_at: Mapped[datetime | None] = mapped_column(
            DateTime(timezone=True), nullable=True, default=None
        )

        def __repr__(self) -> str:
            return f"<AuthUserTokensModel(user_id={self.user_id}, type={self.type}, token_hash={self.token_hash}, expires_at={self.expires_at}, used_at={self.used_at})>"

        def __str__(self) -> str:
            return f"AuthUserTokensModel(user_id={self.user_id}, type={self.type}, expires_at={self.expires_at}, used_at={self.used_at})"

    return AuthUserTokensModel()
