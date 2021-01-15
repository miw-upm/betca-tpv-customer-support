import jwt
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config import Config


class SecurityContext:
    customer = None


class JWTBearer(HTTPBearer):

    def __init__(self, roles: []):
        super(JWTBearer, self).__init__()
        self.roles = roles

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        try:
            payload = jwt.decode(credentials.credentials, Config.jwt_secret, algorithms=["HS256"])
            role: str = payload.get("role")
            if role is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non Role")
            if role not in self.roles:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
            SecurityContext.customer = {"token": credentials.credentials, "mobile": payload.get("user"),
                                        "name": payload.get("name"), "role": role}
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expired token")
