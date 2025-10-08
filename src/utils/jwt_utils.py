import datetime
from functools import wraps

import jwt
from flask import g, request
from pydantic import ValidationError

from src.config import settings
from src.exceptions import UnauthorizedError
from src.schemas.jwt_schemas import JWTPayload


def create_access_token(user_id: int) -> str:
    """
    Creates a signed JWT access token for a given user ID.

    Args:
        user_id (int): The ID of the user.

    Returns:
        str: The encoded JWT access token.

    Raises:
        jwt.PyJWTError: If token encoding fails.
    """
    payload = {
        "sub": str(user_id),
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(seconds=settings.JWT_EXPIRE_IN),
    }
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def decode_token(token: str) -> JWTPayload:
    """
    Decodes and validates a JWT access token.

    Args:
        token (str): The encoded JWT token.

    Returns:
        JWTPayload: The decoded token payload.

    Raises:
        UnauthorizedError: If the token is expired, invalid, or contains invalid data.
    """
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.ExpiredSignatureError as err:
        raise UnauthorizedError("Expired token") from err
    except jwt.PyJWTError as err:
        raise UnauthorizedError("Invalid token") from err

    try:
        return JWTPayload.model_validate(payload)
    except ValidationError as err:
        raise UnauthorizedError("Invalid token data") from err


def jwt_required(f):
    """
    Flask route decorator that enforces JWT authentication.

    Extracts and verifies the 'Authorization: Bearer <token>' header,
    decodes the token, and attaches `user_id` to `flask.g`.

    Args:
        f (Callable): The route function to wrap.

    Returns:
        Callable: The wrapped route function.

    Raises:
        UnauthorizedError: If the header is missing, invalid, or the token is invalid.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            raise UnauthorizedError("Missing or invalid Authorization header.")
        parts = auth_header.split()
        if not parts[0] == "Bearer":
            raise UnauthorizedError("Missing or invalid Bearer header.")
        token = parts[1]
        payload = decode_token(token)
        g.user_id = payload.sub
        return f(*args, **kwargs)

    return decorated
