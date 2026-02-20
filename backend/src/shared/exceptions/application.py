from http import HTTPStatus

from .base import BaseAppError

class ApplicationError(BaseAppError):
	"""Исключения прикладного слоя (use cases)"""
	layer = "application"
	error_code = "application_error"
	http_status = HTTPStatus.BAD_REQUEST  # 400
