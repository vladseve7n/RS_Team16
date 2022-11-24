import os

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from service.api.exceptions import NonAuthorizedError

security = HTTPBearer()

SECRET_KEY = os.getenv('SECRET_KEY')


async def has_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    token = credentials.credentials
    if token == SECRET_KEY:
        return None
    raise NonAuthorizedError()
