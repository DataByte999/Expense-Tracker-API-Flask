from flask import Blueprint, g, jsonify, request

from src.schemas.auth_user_schemas import UpdateUserIn
from src.services.users_service import (
    delete_user_account,
    get_user_info,
    update_user_info,
)
from src.utils.jwt_utils import jwt_required

user_bp = Blueprint("user", __name__, url_prefix="/")


@user_bp.get("/me")
@jwt_required
def get_current_user():
    """
    Retrieve information about logged-in user.

    Returns:
        JSON response (200 OK) containing user data (username, email).
    """
    current_user = get_user_info(g.user_id)
    return jsonify(current_user), 200


@user_bp.patch("/me")
@jwt_required
def patch_current_user():
    """
    Update information for logged-in user.

    Request Body:
        Optional fields: username, email, password

    Returns:
          JSON response (200 OK) containing updated user information.
    """
    request_data = UpdateUserIn.model_validate(request.json).model_dump(
        by_alias=True, exclude_unset=True
    )
    updated_info = update_user_info(g.user_id, request_data)
    return jsonify(updated_info), 200


@user_bp.delete("/me")
@jwt_required
def remove_current_user():
    """
    Delete the logged-in user.

    Returns:
         JSON response (200 OK) containing username and confirmation message.
    """
    deleted_user = delete_user_account(g.user_id)
    return {
        "message": f"User {deleted_user['username']}, was deleted successfully!"
    }, 200
