import jwt
import datetime
from functools import wraps
from flask import request, g
from src.config import settings
from src.exceptions import UnauthorizedError
from src.schemas.jwt_schemas import JWTPayload
from pydantic import ValidationError


def create_access_token(user_id: int) -> str:
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=settings.JWT_EXPIRE_IN),
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Expired token")
    except jwt.PyJWTError:
        raise UnauthorizedError("Invalid token")

    try:
        return JWTPayload.model_validate(payload)
    except ValidationError:
        raise UnauthorizedError("Invalid token data")


def jwt_required(f):
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