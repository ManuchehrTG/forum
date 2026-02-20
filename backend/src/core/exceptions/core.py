# from typing import Any

# class AppError(Exception):
# 	"""Базовое исключение для всех кастомных ошибок."""
# 	def __init__(
# 		self,
# 		message: str,
# 		code: str,
# 		status_code: int = 400,
# 		headers: dict[str, str] | None = None,
# 		**kwargs
# 	):
# 		self.message = message
# 		self.code = code
# 		self.status_code = status_code
# 		self.headers = headers
# 		self.extra = kwargs
# 		super().__init__(self.message)

# class NotFoundError(AppError):
# 	"""Базовое исключение для ненайденных ресурсов"""
# 	def __init__(self, entity: str, entity_id: Any, **kwargs):
# 		super().__init__(
# 			message=f"{entity} not found",
# 			code=f"{entity.lower()}_not_found",
# 			status_code=404,
# 			entity=entity,
# 			entity_id=entity_id,
# 			**kwargs
# 		)

# class ConflictError(AppError):
# 	"""Базовое исключение для конфликтующих операций"""
# 	def __init__(self, message: str, entity: str | None = None, **kwargs):
# 		super().__init__(
# 			message=message,
# 			code="conflict_error",
# 			status_code=409,
# 			entity=entity,
# 			**kwargs
# 		)

# class AuthError(AppError):
# 	"""Базовое исключение для ошибок аутентификации и авторизации"""
# 	def __init__(self, message: str, code: str = "authorization_required", **kwargs):
# 		super().__init__(
# 			message=message,
# 			code=code,
# 			status_code=401,  # По умолчанию 401
# 			**kwargs
# 		)
