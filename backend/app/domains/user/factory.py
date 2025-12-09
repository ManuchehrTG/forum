from .services import UserService, LinkedAccountService

def create_user_service() -> UserService:
	return UserService()

def create_linked_account_service() -> LinkedAccountService:
	return LinkedAccountService()
