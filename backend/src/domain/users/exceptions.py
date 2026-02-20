from uuid import UUID

from src.shared.exceptions import DomainError, BusinessRuleError, NotFoundError, AccessDeniedError

class AuthError(DomainError):
	"""Базовое для всех ошибок аутентификации"""

class InvalidCredentialsError(AuthError):
	"""Неверные учетные данные"""
	error_code = "invalid_credentials"

	def __init__(self, **kwargs):
		message = "Invalid email or password"
		super().__init__(message, **kwargs)


class InvalidTokenError(AuthError):
	"""Невалидный токен"""
	error_code = "invalid_token"

	def __init__(self, message: str | None = None, **kwargs):
		if not message:
			message = f"Invalid token"
		super().__init__(message, **kwargs)


class TokenExpiredError(AuthError):
	"""Просроченный токен"""
	error_code = "expired_token"

	def __init__(self, **kwargs):
		message = f"Expired token"
		super().__init__(message, **kwargs)


class EmailAlreadyExistsError(AuthError, BusinessRuleError):
	"""Email уже зарегистрирован"""
	error_code = "email_already_exists"

	def __init__(self, email: str, **kwargs):
		message = f"Email '{email}' is already registered"
		details = {"email": email}
		super().__init__(message, details=details, **kwargs)


class AccountLockedError(AuthError, AccessDeniedError):
	"""Аккаунт заблокирован"""
	error_code = "account_locked"

	def __init__(self, user_id: str | UUID, reason: str | None = None, **kwargs):
		message = f"Account {user_id} is locked"
		details = {"user_id": user_id, "reason": reason}
		super().__init__(message, details=details, **kwargs)


class UserNotFoundError(NotFoundError):
	"""Пользователь не найден"""
	error_code = "user_not_found"

	def __init__(self, user_id: str | UUID, search_type: str, **kwargs):
		super().__init__(entity="User", entity_id=str(user_id), search_type=search_type, **kwargs)

	@classmethod
	def by_id(cls, user_id: str | UUID, **kwargs) -> "UserNotFoundError":
		return cls(user_id=user_id, search_type="id", **kwargs)

	@classmethod
	def by_provider(cls, provider: str, provider_id: str, **kwargs) -> "UserNotFoundError":
		entity_id = f"{provider}:{provider_id}"
		return cls(user_id=entity_id, search_type="provider", **kwargs)
