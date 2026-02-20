from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from src.core.config import settings
from src.infrastructure.logger import logger
from src.shared.exceptions import BaseAppError

async def base_app_error_handler(request: Request, exc: Exception) -> JSONResponse:
	"""Обработчик для всех наших кастомных исключений"""
	assert isinstance(exc, BaseAppError)

	if exc.original_error:
		logger.error(
			f"Original error for {exc.code}: {exc.original_error}",
			extra={
				"error_code": exc.code,
				"original_error": str(exc.original_error),
				"details": exc.details
			}
		)

	# Определяем HTTP статус
	status_code = getattr(exc, 'http_status', 500)

	# Формируем ответ
	response_data = exc.to_dict()

	# Добавляем trace_id для отслеживания
	response_data["trace_id"] = request.state.trace_id

	return JSONResponse(status_code=status_code, content=response_data)


async def http_exception_handler(request: Request,  exc: Exception) -> JSONResponse:
	"""Обработчик для стандартных HTTPException от FastAPI"""
	assert isinstance(exc, HTTPException)

	if isinstance(exc.detail, dict):
		content = exc.detail.copy()
		content.setdefault("error", "http_error")
	else:
		content = {
			"error": "http_error",
			"message": str(exc.detail),
		}

	content["trace_id"] = request.state.trace_id

	return JSONResponse(
		status_code=exc.status_code,
		content=content,
		headers=exc.headers
	)


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
	"""Обработчик для всех непредвиденных исключений"""
	logger.exception("Unhandled exception", exc_info=exc)

	# В продакшене не показываем детали ошибки
	if settings.debug:
		message = f"Unhandled error: {str(exc)}"
	else:
		message = "Internal server error"

	return JSONResponse(
		status_code=500,
		content={
			"error": "internal_server_error",
			"message": message,
			"trace_id": request.state.trace_id
		}
	)
