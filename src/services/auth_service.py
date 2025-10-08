from pydantic import ValidationError

from src.exceptions import AppError, UnauthorizedError
from src.repositories.users_repo import get_user_by_email, insert_user
from src.schemas.auth_user_schemas import RegisterOut, TokenOut
from src.utils.jwt_utils import create_access_token
from src.utils.password import hash_password, verify_password


def create_user(username: str, email: str, password: str) -> dict:
    """
    Create a new user account.

    The password is securely hashed before being stored in the database.

    Args:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
          dict: Created user information (username, email).

    Raises:
          AppError: If schema validation fails.
    """
    hashed_password = hash_password(password)
    created_user = insert_user(username, email, hashed_password)
    try:
        return RegisterOut.model_validate({"user": created_user}).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def authenticate(email: str, password: str) -> dict:
    """
    Authenticates a user by email and password.
    Verifies the password and creates access token.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        dict: Token type and access token.
    Raises:
        UnauthorizedError: If email or password is incorrect.
        AppError: If schema validation fails.
    """
    user_record = get_user_by_email(email)
    if not user_record or not verify_password(password, user_record["password_hash"]):
        raise UnauthorizedError("Invalid credentials")
    access_token = create_access_token(user_record["id"])
    try:
        return TokenOut.model_validate({"access_token": access_token}).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err
