from datetime import datetime

from pydantic import ConfigDict, Field
from pydantic.main import BaseModel


class CurrentSessionResponseSchema(BaseModel):
    """
    Schema for the current session response.
    """

    uuid: str = Field(..., description="The unique identifier for the session.")
    device: str | None = Field(
        None, description="Information about the device used for the session."
    )
    ip_address: str | None = Field(
        None, description="The IP address from which the session was initiated."
    )
    browser: str | None = Field(
        default=None, description="Information about the browser used for the session."
    )
    revoked_at: datetime | None = Field(
        default=None,
        description="Timestamp indicating when the session was revoked, if applicable.",
    )
    expires_at: datetime = Field(
        ..., description="Timestamp indicating when the session will expire."
    )
    is_active: bool = Field(
        ..., description="Indicates whether the session is currently active."
    )

    model_config = ConfigDict(
        from_attributes=True,
    )
