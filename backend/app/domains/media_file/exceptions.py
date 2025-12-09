from app.core.exceptions import AppError, ValidationError

class MediaFileError(AppError):
	def __init__(self, message: str, **kwargs):
		super().__init__(
			message=message,
			code="media_file_error",
			status_code=400,
			**kwargs
		)


class ValidateFileError(ValidationError):
	def __init__(self, message: str, **kwargs):
		super().__init__(
			message=message,
			code="file_validation_error",
			status_code=422,
			**kwargs
		)

class MediaFilesExpiredError(AppError):
	def __init__(self, message: str):
		super().__init__(
			message="Media file(s) have expired",
			code="media_files_expired",
			status_code=410
		)