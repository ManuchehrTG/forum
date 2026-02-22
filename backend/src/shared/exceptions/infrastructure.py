from http import HTTPStatus

from .base import BaseAppError

class InfrastructureError(BaseAppError):
	"""Исключения инфраструктурного слоя (5xx)"""
	layer = "infrastructure"
	error_code = "infrastructure_error"
	http_status = HTTPStatus.SERVICE_UNAVAILABLE  # 503


class DatabaseError(InfrastructureError):
	"""Ошибки базы данных"""
	error_code = "database_error"
	http_status = HTTPStatus.INTERNAL_SERVER_ERROR  # 500


class ExternalServiceError(InfrastructureError):
	"""Ошибки внешних сервисов"""
	error_code = "external_service_error"

	def __init__(self, service: str, original_error: Exception | None = None, **kwargs):
		message = f"Service '{service}' is unavailable"
		details = {"service": service}
		super().__init__(message, details=details, original_error=original_error, **kwargs)
