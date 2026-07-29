from pydantic import Field
from pydantic.main import BaseModel


class AuthEmailVerifySchema(BaseModel):
    token: str = Field(..., min_length=6, max_length=6)
