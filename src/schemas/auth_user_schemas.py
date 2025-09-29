from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Literal, Optional


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
    token_type: Literal["Bearer"] = "Bearer"


class UpdateUserIn(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, serialization_alias="password_hash")

class UpdateUserOut(UserOut):
    password: Literal["********"] = "********"


class DeleteUserOut(BaseModel):
    username: Annotated[str, Field(min_length=3, max_length=50)]