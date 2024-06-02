import sys

sys.path.append(".")

from fastapi import Security, status
from fastapi.security.api_key import APIKeyHeader

from api.db.models.users import User
from api.exceptions.base import DiaryServerHTTPException

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def validate_token(auth_key_header: str = Security(api_key_header)) -> User:
    if auth_key_header is None:
        raise DiaryServerHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No Key passed")

    user_id = User.verify_auth_token(auth_key_header)
    user = User.get_user_by_id(user_id)
    if user is None:
        raise DiaryServerHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Key")

    return user