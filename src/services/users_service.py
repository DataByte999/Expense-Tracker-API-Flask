from pydantic import ValidationError

from src.exceptions import AppError, BadRequestError, NotFoundError
from src.repositories.users_repo import delete_user, get_user, update_user
from src.schemas.auth_user_schemas import DeleteUserOut, UpdateUserOut, UserOut
from src.utils.password import hash_password


def get_user_info(user_id: int) -> dict:
    """
    Retrieve a user's information by ID.

    Args:
        user_id (int): The unique identifier of the user.

    Returns:
          dict: Validated user information (username, email).

    Raises:
          NotFoundError: If no user exist with the given ID.
          AppError: If schema validation fails.
    """
    user_info = get_user(user_id)
    if not user_info:
        raise NotFoundError("User not found")
    try:
        return UserOut.model_validate(user_info).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def update_user_info(user_id: int, data: dict) -> dict:
    """
    Update a user's information with given data by ID.

    Args:
        user_id (int): ID of the user to update.
        data (dict): Fields to update (e.g. username, email, password_hash).

    Returns:
          dict: Updated user information.

    Raises:
          BadRequestError: If data is empty.
          NotFoundError: If no user exist with the given ID.
          AppError: If schema validation fails.
    """
    if not data:
        raise BadRequestError("No data provided")
    if "password_hash" in data:
        pwd = data.get("password_hash")
        data["password_hash"] = hash_password(pwd)
    updated_info = update_user(user_id, data)
    if not updated_info:
        raise NotFoundError("User not found")
    try:
        return UpdateUserOut.model_validate(updated_info).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err


def delete_user_account(user_id: int) -> dict:
    """
    Delete a user by their ID.

    Args:
        user_id (int): ID of the user to delete.

    Returns:
          dict: Username of deleted user.

    Raises:
          NotFoundError: If no user exist with the given ID.
          AppError: If schema validation fails.
    """
    deleted_username = delete_user(user_id)
    if not deleted_username:
        raise NotFoundError("User not found")
    try:
        return DeleteUserOut.model_validate(deleted_username).model_dump()
    except ValidationError as err:
        raise AppError("Internal schema validation error") from err
