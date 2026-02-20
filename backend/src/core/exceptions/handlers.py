# from typing import Mapping
# from fastapi import Request
# from fastapi.exceptions import RequestValidationError, HTTPException
# from fastapi.responses import JSONResponse

# from .core import AppError
# from src.infrastructure.logger import logger

# def _error_response(status_code: int, code: str, message: str, headers: Mapping[str, str] | None = None, **kwargs) -> JSONResponse:
# 	"""Универсальный конструктор error-ответов"""
# 	content = {
# 		"error": {
# 			"code": code,
# 			"message": message,
# 			**kwargs
# 		}
# 	}
# 	return JSONResponse(
# 		content=content,
# 		status_code=status_code,
# 		headers=headers or {}
# 	)

# async def handle_app_error(request: Request, exc: Exception) -> JSONResponse:
# 	"""Обработчик для кастомных исключений AppError и его потомков"""
# 	assert isinstance(exc, AppError)
# 	log_level = "warning" if exc.status_code < 500 else "error"

# 	getattr(logger, log_level)(
# 		"AppError: %s (code: %s, status: %d)",
# 		exc.message, exc.code, exc.status_code,
# 		extra=exc.extra
# 	)

# 	return _error_response(
# 		status_code=exc.status_code,
# 		code=exc.code,
# 		message=exc.message,
# 		headers=exc.headers,
# 		**exc.extra
# 	)

# async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
# 	"""Обработчик ошибок валидации Pydantic"""
# 	assert isinstance(exc, RequestValidationError)
# 	logger.warning("Validation error: %s", exc.errors())
# 	return _error_response(
# 		status_code=422,
# 		code="validation_error",
# 		message="Ошибка валидации данных",
# 		details=exc.errors()
# 	)

# async def handle_http_exception(request: Request, exc: Exception) -> JSONResponse:
# 	"""Обработчик стандартных HTTPException"""
# 	assert isinstance(exc, HTTPException)
# 	logger.warning("HTTPException: %s (status: %d)", exc.detail, exc.status_code)
# 	return _error_response(
# 		status_code=exc.status_code,
# 		code=f"http_{exc.status_code}",
# 		message=str(exc.detail),
# 		headers=exc.headers
# 	)

# async def handle_generic_error(request: Request, exc: Exception) -> JSONResponse:
# 	"""Обработчик для непредвиденных исключений"""
# 	logger.error("Unhandled exception %s", exc, exc_info=exc)
# 	return _error_response(
# 		status_code=500,
# 		code="internal_server_error",
# 		message="Внутренняя ошибка сервера"
# 	)
