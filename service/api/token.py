from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from service.api.exceptions import NonAuthorizedError
from service.settings import get_config

security = HTTPBearer()
service_config = get_config()


async def has_access(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> None:
    token = credentials.credentials
    if token == service_config.SECRET_KEY:
        return None
    raise NonAuthorizedError()
