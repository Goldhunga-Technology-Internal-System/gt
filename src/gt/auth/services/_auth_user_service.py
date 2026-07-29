from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.models._auth_user_session_model import AuthUserSessionModelBase
from gt.auth.repositories._auth_user_session_repository import TSession
from gt.auth.services._auth_user_session_service import (
    AuthUserSessionService,
    get_auth_user_session_service,
)
from gt.exceptions import ConflictException, DomainException

from ..events import UserCreatedEvent, event_bus
from ..models import AuthUserModel
from ..repositories import AuthUserRepository
from ..repositories._auth_user_account_repository import TAccount
from ..services import AuthUserAccountService
from ..services._auth_user_account_service import (
    ACCOUNT_TYPE_LITERAL,
    get_auth_user_account_service,
)


class AuthUserService[TSession: AuthUserSessionModelBase]:
    """
    Service class for handling authentication-related operations for users.
    """

    def __init__(
        self,
        repository: AuthUserRepository,
        model: type[AuthUserModel],
        account_service: AuthUserAccountService,
        session_service: AuthUserSessionService[TSession],
    ):
        """
        Initialize the AuthUserService with a user repository.
        """

        self._repository = repository
        self._model = model
        self._account_service = account_service
        self._session_service = session_service

    async def create_user(
        self,
        user: AuthUserModel,
        password: str | None,
        ip_address: str,
        device: str,
        browser: str,
        session_expire_minutes: int,
    ) -> tuple[AuthUserModel, TSession]:
        """
        Create a new user instance.
        """
        try:
            check_existing_user = await self._repository.get_by(email=user.email)
            if check_existing_user:
                raise ConflictException(
                    error=f"User with email {user.email} already exists.",
                    errors={"email": "This email is already registered."},
                )
            new_user = await self._repository.add(user)

            await self._add_user_account(
                user_id=new_user.id, type="credentials", password=password
            )

            session = await self._create_user_session(
                user_id=new_user.id,
                expire_minutes=session_expire_minutes,
                device=device,
                ip_address=ip_address,
                browser=browser,
            )

            await event_bus.publish(
                UserCreatedEvent(user_id=new_user.id, user_uuid=new_user.uuid)
            )
            return new_user, session
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to create user.",
                internal_details=str(e),
            ) from e

    async def _add_user_account(
        self,
        user_id: int,
        type: ACCOUNT_TYPE_LITERAL,
        password: str | None = None,
        provider: str | None = None,
    ) -> None:
        """
        Add a user account for the specified user.
        """
        try:
            await self._account_service.create_account(
                user_id=user_id, type=type, password=password, provider=provider
            )
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to add user account.",
                internal_details=str(e),
            ) from e

    async def get_user_by(self, **kwargs) -> AuthUserModel | None:
        """
        Retrieve a user instance based on provided keyword arguments.
        """
        try:
            return await self._repository.get_by(**kwargs)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to retrieve user.",
                internal_details=str(e),
            ) from e

    async def _create_user_session(
        self,
        user_id: int,
        expire_minutes: int,
        device: str,
        ip_address: str,
        browser: str,
    ) -> TSession:
        """
        Create a new user session.
        """
        try:
            session = await self._session_service.create_session(
                user_id=user_id,
                expire_minutes=expire_minutes,
                device=device,
                ip_address=ip_address,
                browser=browser,
            )
            return session
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to create user session.",
                internal_details=str(e),
            ) from e


def get_auth_user_service(
    *,
    session: AsyncSession,
    user_model: type[AuthUserModel],
    account_model: type[TAccount],
    session_model: type[TSession],
) -> AuthUserService:
    """
    Factory function to create an instance of AuthUserService.

    :param session: An instance of AsyncSession for database operations.
    :return: An instance of AuthUserService.
    """
    repository = AuthUserRepository(session=session, model=user_model)
    user_account_service = get_auth_user_account_service(
        session=session, model=account_model
    )
    user_session_service = get_auth_user_session_service(
        session=session, model=session_model
    )
    return AuthUserService(
        repository=repository,
        model=user_model,
        account_service=user_account_service,
        session_service=user_session_service,
    )
