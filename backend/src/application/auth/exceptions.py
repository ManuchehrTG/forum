from src.shared.exceptions import ApplicationError
from src.domain.users.exceptions import AuthError

class AuthFailedError(ApplicationError):
	"""Общая ошибка аутентификации на уровне приложения"""
	error_code = "auth_failed"

	def __init__(self, reason: str, original_error: AuthError | None = None, **kwargs):
		message = f"Authentication failed: {reason}"
		details = {"reason": reason}
		if original_error:
			details["original_error"] = original_error.code
		super().__init__(message, details=details, **kwargs)


class RateLimitExceededError(ApplicationError):
	"""Превышен лимит запросов"""
	error_code = "rate_limit_exceeded"
	http_status = 429

	def __init__(self, limit: int, window: str, **kwargs):
		message = f"Rate limit exceeded: {limit} requests per {window}"
		details = {"limit": limit, "window": window}
		super().__init__(message, details=details, **kwargs)
