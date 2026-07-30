from pydantic import Field
from pydantic.main import BaseModel


class AuthEmailVerifySchema(BaseModel):
    token: str = Field(...)
