# from fastapi import FastAPI
# from fastapi.exceptions import RequestValidationError, HTTPException

# from .core import AppError, NotFoundError, ConflictError, AuthError
# from .handlers import handle_app_error, handle_validation_error, handle_http_exception, handle_generic_error

# def setup_exception_handlers(app: FastAPI) -> None:
# 	"""Регистрация всех обработчиков исключений"""
# 	# Все потомки AppError обрабатываются одним обработчиком
# 	app.add_exception_handler(AppError, handle_app_error)
# 	app.add_exception_handler(RequestValidationError, handle_validation_error)
# 	app.add_exception_handler(HTTPException, handle_http_exception)
# 	app.add_exception_handler(Exception, handle_generic_error)
