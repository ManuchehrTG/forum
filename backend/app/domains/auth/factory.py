from app.domains.user.services import UserService, LinkedAccountService
from .services import AuthService

def create_auth_service() -> AuthService:
	return AuthService(
		user_service=UserService(),
		linked_account_service=LinkedAccountService()
	)
