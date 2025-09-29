from src.repositories.users_repo import get_user, update_user, delete_user
from src.schemas.auth_user_schemas import UserOut, UpdateUserOut, DeleteUserOut
from pydantic import ValidationError
from src.exceptions import AppError, translate_db_errors, NotFoundError
from src.utils.password import hash_password
from psycopg import Error as PsycopgError


def get_user_by_id(user_id: int):
    try:
        user_data = get_user(user_id)
        if not user_data:
            raise NotFoundError("User not found")
        return UserOut.model_validate(user_data).model_dump()

    except PsycopgError as e:
        raise translate_db_errors(e)

    except ValidationError as e:
        raise AppError("Internal schema validation error")



def user_update(user_id: int, data: dict) -> dict:
    if "password_hash" in data:
        pwd = data.get("password_hash")
        data["password_hash"] = hash_password(pwd)

    try:
        updated_info = update_user(user_id, data)
        if not updated_info:
            raise NotFoundError("User not found")
        return UpdateUserOut.model_validate(updated_info).model_dump()

    except PsycopgError as e:
        raise translate_db_errors(e)

    except ValidationError as e:
        raise AppError("Internal schema validation error")



def user_delete(user_id: int) -> dict:

    try:
        deleted_username = delete_user(user_id)
        if not deleted_username:
            raise NotFoundError("User not found")
        return DeleteUserOut.model_validate(deleted_username).model_dump()

    except PsycopgError as e:
        raise translate_db_errors(e)

    except ValidationError as e:
        raise AppError("Internal schema validation error")
