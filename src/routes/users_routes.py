from flask import Blueprint, request, jsonify, g
from src.services.users_service import get_user_by_id, user_update, user_delete
from src.utils.jwt_utils import jwt_required
from src.schemas.auth_user_schemas import UpdateUserIn
from pydantic import ValidationError
from src.exceptions import BadRequestError


user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.get("/")
@jwt_required
def user_info():
    user = get_user_by_id(g.user_id)
    return jsonify(user), 200


@user_bp.patch("/update")
@jwt_required
def update_user():
    try:
        payload = UpdateUserIn.model_validate(request.json).model_dump(by_alias=True, exclude_unset=True)
    except ValidationError as e:
        raise  BadRequestError(str(e))
    updated_info = user_update(g.user_id, payload)
    return jsonify(updated_info), 200


@user_bp.delete("/delete")
@jwt_required
def delete_user():
    deleted_user = user_delete(g.user_id)
    return {"message": f"User {deleted_user["username"]}, was deleted successfully!"}, 200