from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.models import AuthUserModel
from gt.exceptions import CreateException


class AuthUserRepository:
    """
    Auth user repository class for managing user authentication and related operations.
    """

    def __init__(self, session: AsyncSession, model: type[AuthUserModel]):
        """
        Initialize the AuthUserRepository with a database session and a model.
        """

        self.session = session
        self.model = model

    async def add(self, user: AuthUserModel) -> AuthUserModel:
        """
        Add a new user to the database.
        """
        try:
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            return user
        except Exception as e:
            raise CreateException(
                error="Failed to add user to the database.",
                internal_details=str(e),
            ) from e

    async def get_by(self, **kwargs) -> AuthUserModel | None:
        """
        Retrieve a user from the database based on provided keyword arguments.
        """
        try:
            stmt = select(self.model).filter_by(**kwargs)
            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()
            return user
        except Exception as e:
            raise CreateException(
                error="Failed to retrieve user from the database.",
                internal_details=str(e),
            ) from e
