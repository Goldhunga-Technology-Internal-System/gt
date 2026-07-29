from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from gt.auth.models._auth_user_onboarding_model import AuthUserOnboardingModelBase
from gt.exceptions import CreateException


class AuthUserOnboardingRepository[TOnboarding: AuthUserOnboardingModelBase]:
    def __init__(self, session: AsyncSession, model: type[TOnboarding]):
        self.session = session
        self.model = model

    async def add(self, onboarding: TOnboarding) -> TOnboarding:
        try:
            self.session.add(onboarding)
            await self.session.flush()
            await self.session.refresh(onboarding)
            return onboarding
        except Exception as e:
            raise CreateException(
                error="Failed to add onboarding to the database.",
                internal_details=str(e),
            ) from e

    async def get_by(self, **kwargs) -> TOnboarding | None:
        try:
            stmt = select(self.model).filter_by(**kwargs)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except Exception as e:
            raise CreateException(
                error="Failed to retrieve onboarding from the database.",
                internal_details=str(e),
            ) from e
