from src.schemas.auth_user_schemas import RegisterOut, TokenOut
from src.exceptions import UnauthorizedError, AppError
from src.repositories.users_repo import insert_user, get_user_by_email
from src.utils.password import hash_password, verify_password
from src.utils.jwt_utils import create_access_token
from pydantic import ValidationError



def create_user(username: str, email: str, password: str) -> dict:
    pwd_hash = hash_password(password)
    user = insert_user(username, email, pwd_hash)
    try:
        return RegisterOut.model_validate({"user": user}).model_dump()
    except ValidationError as e:
        raise  AppError("Internal schema validation error")


def authenticate(email: str, password: str) -> str:
    user = get_user_by_email(email)
    if not user or not verify_password(password, user["password_hash"]):
        raise UnauthorizedError("Invalid credentials")
    token = create_access_token(user["id"])
    try:
        return TokenOut.model_validate({"access_token": token}).model_dump()
    except ValidationError as e:
        raise  AppError("Internal schema validation error")
