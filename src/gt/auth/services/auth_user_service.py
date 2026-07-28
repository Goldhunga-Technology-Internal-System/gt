from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.events import UserCreatedEvent, event_bus
from gt.exceptions import ConflictException, DomainException

from ..models.auth_user_model import AuthUserModel
from ..repositories.auth_user_repository import AuthUserRepository


class AuthUserService:
    """
    Service class for handling authentication-related operations for users.
    """

    def __init__(self, repository: AuthUserRepository, model: type[AuthUserModel]):
        """
        Initialize the AuthUserService with a user repository.
        """

        self.repository = repository
        self.model = model

    async def create_user(self, user: AuthUserModel) -> AuthUserModel:
        """
        Create a new user instance.

        :param kwargs: Keyword arguments for user attributes.
        :return: An instance of AuthUserModel.
        """
        try:
            check_existing_user = await self.repository.get_by(email=user.email)
            if check_existing_user:
                raise ConflictException(
                    error=f"User with email {user.email} already exists.",
                    errors={"email": "This email is already registered."},
                )
            new_user = await self.repository.add(user)
            await event_bus.publish(
                UserCreatedEvent(user_id=new_user.id, user_uuid=new_user.uuid)
            )
            return new_user
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to create user.",
                internal_details=str(e),
            ) from e

    async def get_user_by(self, **kwargs) -> AuthUserModel | None:
        """
        Retrieve a user instance based on provided keyword arguments.

        :param kwargs: Keyword arguments for user attributes.
        :return: An instance of AuthUserModel or None if not found.
        """
        try:
            return await self.repository.get_by(**kwargs)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to retrieve user.",
                internal_details=str(e),
            ) from e


def get_auth_user_service(
    session: AsyncSession, model: type[AuthUserModel]
) -> AuthUserService:
    """
    Factory function to create an instance of AuthUserService.

    :param session: An instance of AsyncSession for database operations.
    :return: An instance of AuthUserService.
    """
    repository = AuthUserRepository(session=session, model=model)
    return AuthUserService(repository=repository, model=model)
