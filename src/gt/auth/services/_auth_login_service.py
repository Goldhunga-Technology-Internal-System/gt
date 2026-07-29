from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.models._auth_user_account_model import AuthUserAccountModelBase
from gt.auth.models._auth_user_model import TUser
from gt.auth.models._auth_user_session_model import AuthUserSessionModelBase
from gt.exceptions import DomainException
from gt.exceptions._base_exceptions import InvalidException

from ..models import AuthUserModel
from ..repositories import AuthUserRepository
from ..repositories._auth_user_account_repository import TAccount
from ..repositories._auth_user_session_repository import TSession
from ..services._auth_user_account_service import (
    AuthUserAccountService,
    get_auth_user_account_service,
)
from ..services._auth_user_session_service import (
    AuthUserSessionService,
    get_auth_user_session_service,
)
from ..services.hash._hash_service import HasherService


class AuthLoginService[
    TUser: AuthUserModel,
    TAccount: AuthUserAccountModelBase,
    TSession: AuthUserSessionModelBase,
]:
    """
    Service for handling user login functionality.
    """

    def __init__(
        self,
        user_repository: AuthUserRepository,
        user_model: type[TUser],
        account_service: AuthUserAccountService[TAccount],
        session_service: AuthUserSessionService[TSession],
        hash_service: HasherService,
    ):
        self._user_repository = user_repository
        self._user_model = user_model
        self._account_service = account_service
        self._session_service = session_service
        self._hash_service = hash_service

    async def login(
        self,
        email: str,
        password: str,
        ip_address: str,
        device: str,
        browser: str,
        session_expire_minutes: int,
    ) -> tuple[TUser, TSession]:
        """
        Authenticate a user with the provided email and password.
        """
        try:
            user = await self._user_repository.get_by(email=email.lower())
            if not user:
                self._hash_service.dummy_verify(password)
                raise InvalidException(
                    error="Invalid email or password.",
                    errors={"email": "Invalid email or password."},
                )

            account = await self._account_service.get_account_by(
                user_id=user.id, type="credentials"
            )
            if not account or not account.hashed_password:
                self._hash_service.dummy_verify(password)
                raise InvalidException(
                    error="Invalid email or password.",
                    errors={"email": "Invalid email or password."},
                )

            if not self._hash_service.verify(account.hashed_password, password):
                raise InvalidException(
                    error="Invalid email or password.",
                    errors={"email": "Invalid email or password."},
                )

            session = await self._session_service.create_session(
                user_id=user.id,
                expire_minutes=session_expire_minutes,
                device=device,
                ip_address=ip_address,
                browser=browser,
            )

            ## MFA checking required

            return user, session
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to login.",
                internal_details=str(e),
            ) from e

    async def logout(self, session_uuid: str) -> None:
        """
        Logout a user by invalidating their session.
        """
        try:
            await self._session_service.invalidate_session(session_uuid=session_uuid)
        except DomainException:
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to logout.",
                internal_details=str(e),
            ) from e


def get_auth_login_service(
    *,
    session: AsyncSession,
    user_model: type[TUser],
    account_model: type[TAccount],
    session_model: type[TSession],
) -> AuthLoginService[TUser, TAccount, TSession]:
    """
    Factory function to create an instance of AuthLoginService with the provided dependencies.
    """
    repository = AuthUserRepository(session=session, model=user_model)
    account_service = get_auth_user_account_service(
        session=session, model=account_model
    )
    session_service = get_auth_user_session_service(
        session=session, model=session_model
    )
    hash_service = HasherService()
    return AuthLoginService(
        user_repository=repository,
        user_model=user_model,
        account_service=account_service,
        session_service=session_service,
        hash_service=hash_service,
    )
