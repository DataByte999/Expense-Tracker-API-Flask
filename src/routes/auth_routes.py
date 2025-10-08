from flask import Blueprint, jsonify, request

from src.schemas.auth_user_schemas import LoginIn, RegisterIn
from src.services.auth_service import authenticate, create_user

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    """
    Create a new user account.

    Request Body:
        username (str): User's username.
        email (str): User's email address.
        password (str): User's password.

    Returns:
          JSON response (201 Created) containing registered user's information.
    """
    request_data = RegisterIn.model_validate(request.json)
    created_user = create_user(
        request_data.username, str(request_data.email), request_data.password
    )
    return jsonify(created_user), 201


@auth_bp.post("/login")
def login():
    """
    Authenticate a user and issue an access token.

    Request Body:
        email (str): User's email address.
        password (str): User's password.

    Returns:
          JSON response (200 OK) containing token type and access token.
    """
    request_data = LoginIn.model_validate(request.json)
    token_data = authenticate(str(request_data.email), request_data.password)
    return jsonify(token_data), 200
