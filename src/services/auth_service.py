from src.schemas.auth_user_schemas import RegisterOut, TokenOut
from src.exceptions import UnauthorizedError, AppError
from src.repositories.users_repo import insert_user, get_user_by_email
from src.utils.password import hash_password, verify_password
from src.utils.jwt_utils import create_access_token
from src.exceptions import translate_db_errors
from pydantic import ValidationError
from psycopg import Error as PsycopgError


def create_user(username: str, email: str, password: str) -> dict:
    pwd_hash = hash_password(password)

    try:
        user = insert_user(username, email, pwd_hash)
        return RegisterOut.model_validate({"user": user}).model_dump()

    except PsycopgError as e:
        raise translate_db_errors(e)

    except ValidationError as e:
        raise  AppError("Internal schema validation error")


def authenticate(email: str, password: str) -> str:
    try:
        user = get_user_by_email(email)
        if not user or not verify_password(password, user["password_hash"]):
            raise UnauthorizedError("Invalid credentials")

        token = create_access_token(user["id"])
        return TokenOut.model_validate({"access_token": token}).model_dump()

    except PsycopgError as e:
        raise translate_db_errors(e)

    except ValidationError as e:
        raise  AppError("Internal schema validation error")