from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field


class UserOut(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr


class RegisterIn(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class RegisterOut(BaseModel):
    message: Literal["User registered successfully"] = "User registered successfully"
    user: UserOut


class LoginIn(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8)]


class TokenOut(BaseModel):
    access_token: str
    token_type: Literal["Bearer"] = "Bearer"  # noqa S105


class UpdateUserIn(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str | None = Field(
        None, min_length=8, serialization_alias="password_hash"
    )


class UpdateUserOut(UserOut):
    password: Literal["********"] = "********"  # noqa S105


class DeleteUserOut(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]
