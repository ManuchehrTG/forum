from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.domains.user.schemas import User
from .exceptions import TokenExpiredError, InvalidTokenError
from .factory import create_auth_service
from .services import AuthService

bearer_scheme = HTTPBearer()

def get_auth_service() -> AuthService:
	return create_auth_service()

async def get_current_user(
	credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
	auth_service: AuthService = Depends(get_auth_service)
) -> User:
	token = credentials.credentials
	if not token:
		raise HTTPException(401, "Token is required")

	return await auth_service.get_user_by_token(token=token)
