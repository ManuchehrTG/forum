from fastapi import FastAPI, HTTPException

from src.core.config import settings
from src.shared.exceptions import BaseAppError
from .exceptions.handlers import (
	base_app_error_handler,
	http_exception_handler,
	generic_exception_handler
)

def create_app() -> FastAPI:
	app = FastAPI(
		title=settings.app.title,
		version="1.0.0",
	)

	# Или если нужно добавить после создания
	app.add_exception_handler(BaseAppError, base_app_error_handler)
	app.add_exception_handler(HTTPException, http_exception_handler)
	app.add_exception_handler(Exception, generic_exception_handler)

	return app
