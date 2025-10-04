from flask import Blueprint, request, jsonify
from src.services.auth_service import create_user, authenticate
from src.schemas.auth_user_schemas import RegisterIn, LoginIn



auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    payload = RegisterIn.model_validate(request.json)
    user_data = create_user(payload.username, payload.email, payload.password)
    return jsonify(user_data), 201


@auth_bp.post("/login")
def login():
    payload = LoginIn.model_validate(request.json)
    token = authenticate(payload.email, payload.password)
    return jsonify(token), 200
