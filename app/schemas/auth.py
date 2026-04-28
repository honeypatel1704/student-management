from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


RoleType = Literal["admin", "user", "agent", "student"]


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: RoleType = "user"

    @model_validator(mode="after")
    def validate_student_email(self):
        # Enforce student email policy: domain must be vrinsoft.com and
        # the local part cannot be purely numeric (e.g., 123456@vrinsoft.com).
        if self.role == "student":
            local, _, domain = str(self.email).partition("@")
            if domain.lower() != "vrinsoft.com":
                raise ValueError("Student email must use the @vrinsoft.com domain")
            if local.isdigit():
                raise ValueError("Student email local-part cannot be only digits")
        return self


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr
    role: RoleType
    is_active: bool
    created_at: datetime
    updated_at: datetime
