from typing import Literal

from pydantic import BaseModel, Field


class AuthOnboardingRegisterSchema(BaseModel):
    """
    Schema for user onboarding registration.
    """

    theme: Literal["light", "dark", "auto"] = Field(default="light", max_length=20)
    referral_source: str | None = Field(default=None, max_length=255)
