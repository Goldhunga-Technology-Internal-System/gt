from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.models._auth_user_model import AuthUserModel, TUser
from gt.auth.models._auth_user_tokens_model import AuthUserTokensModelBase
from gt.auth.repositories._auth_user_repository import AuthUserRepository
from gt.auth.repositories._auth_user_tokens_repository import TToken
from gt.auth.services._auth_user_tokens_service import AuthUserTokensService
from gt.auth.services.hash._hash_service import HasherService
from gt.exceptions._base_exceptions import (
    ConflictException,
    DomainException,
    InvalidException,
    NotFoundException,
)


class AuthEmailService[TUser: AuthUserModel, TToken: AuthUserTokensModelBase]:
    """
    Service class for handling email verification operations.
    """

    def __init__(
        self,
        user_repository: AuthUserRepository[TUser],
        token_service: AuthUserTokensService[TToken],
        hash_service: HasherService,
    ):
        self._user_repository = user_repository
        self._token_service = token_service
        self._hash_service = hash_service

    async def verify_email(self, user: TUser, token: str) -> TUser:
        """
        Verify a user's email address using a verification token.
        """
        try:
            if user.is_email_verified():
                raise ConflictException(
                    error="Email is already verified.",
                    errors={"code": "EMAIL_ALREADY_VERIFIED"},
                )

            token_record = await self._token_service.get_token_by(
                user_id=user.id,
                type="email_verification",
                used_at=None,
            )
            if not token_record:
                raise NotFoundException(
                    error="No verification token found. Request a new one.",
                )

            if token_record.expires_at < datetime.now(UTC):
                raise InvalidException(
                    error="Verification token has expired. Request a new one.",
                )

            if not self._hash_service.verify_deterministic_hash(
                token, token_record.token_hash
            ):
                raise InvalidException(
                    error="Invalid verification token.",
                )

            token_record.used_at = datetime.now(UTC)
            await self._token_service.update_token(token_record)

            user.email_verified_at = datetime.now(UTC)
            await self._user_repository.update(user)

            return user
        except (
            NotFoundException,
            ConflictException,
            InvalidException,
            DomainException,
        ):
            raise
        except Exception as e:
            raise DomainException(
                error="Failed to verify email.",
                internal_details=str(e),
            ) from e


def get_auth_email_service(
    *,
    session: AsyncSession,
    user_model: type[TUser],
    token_model: type[TToken],
) -> AuthEmailService[TUser, TToken]:
    """
    Factory function to create an instance of AuthEmailService.
    """
    from gt.auth.services._auth_user_tokens_service import (
        get_auth_user_tokens_service,
    )

    user_repository = AuthUserRepository(session=session, model=user_model)
    token_service = get_auth_user_tokens_service(session=session, model=token_model)
    hash_service = HasherService()
    return AuthEmailService(
        user_repository=user_repository,
        token_service=token_service,
        hash_service=hash_service,
    )
