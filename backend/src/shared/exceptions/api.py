from http import HTTPStatus

from .base import BaseAppError

class ApiError(BaseAppError):
	"""Исключения API слоя"""
	layer = "api"
	error_code = "api_error"
	http_status = HTTPStatus.INTERNAL_SERVER_ERROR

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.http_status = self.http_status

class UnauthorizedError(ApiError):
	"""401 Unauthorized"""
	error_code = "unauthorized"
	http_status = HTTPStatus.UNAUTHORIZED

class ForbiddenError(ApiError):
	"""403 Forbidden"""
	error_code = "forbidden"
	http_status = HTTPStatus.FORBIDDEN

class NotFoundApiError(ApiError):
	"""404 Not Found"""
	error_code = "not_found"
	http_status = HTTPStatus.NOT_FOUND
