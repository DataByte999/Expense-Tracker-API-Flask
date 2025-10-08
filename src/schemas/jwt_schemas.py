from pydantic import BaseModel


class JWTPayload(BaseModel):
    sub: int
    exp: int
