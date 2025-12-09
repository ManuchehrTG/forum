from fastapi import Depends, HTTPException

from .factory import create_user_service, create_linked_account_service
from .services import UserService, LinkedAccountService

def get_user_service() -> UserService:
	return create_user_service()

def get_linked_account_service() -> LinkedAccountService:
	return create_linked_account_service()
