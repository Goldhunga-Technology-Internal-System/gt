from pydantic import Field, model_validator
from pydantic.main import BaseModel


class AuthUserRegisterSchema(BaseModel):
    """
    Schema for user registration.
    """

    email: str
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str | None = None

    @model_validator(mode="after")
    def calculate_full_name(self):
        """
        Calculate the full name from the email if not provided.
        """
        if not self.full_name:
            username = self.email.split("@", 1)[0]
            self.full_name = (
                username.replace(".", " ").replace("_", " ").replace("-", " ").title()
            )
        return self
