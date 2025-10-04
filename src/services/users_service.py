from src.repositories.users_repo import get_user, update_user, delete_user
from src.schemas.auth_user_schemas import UserOut, UpdateUserOut, DeleteUserOut
from pydantic import ValidationError
from src.exceptions import AppError, NotFoundError, BadRequestError
from src.utils.password import hash_password



def get_user_by_id(user_id: int):
    user_data = get_user(user_id)
    if not user_data:
        raise NotFoundError("User not found")
    try:
        return UserOut.model_validate(user_data).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def user_update(user_id: int, data: dict) -> dict:
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
    except ValidationError as e:
        raise AppError("Internal schema validation error")


def user_delete(user_id: int) -> dict:
    deleted_username = delete_user(user_id)
    if not deleted_username:
        raise NotFoundError("User not found")
    try:
        return DeleteUserOut.model_validate(deleted_username).model_dump()
    except ValidationError as e:
        raise AppError("Internal schema validation error")
