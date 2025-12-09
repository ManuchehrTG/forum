from fastapi import UploadFile

from .exceptions import ValidateFileError

class MediaFileValidator:
	MIME_TO_CATEGORY = {
		# Фото
		"image/jpeg": "photo",
		"image/jpg": "photo", 
		"image/png": "photo",
		"image/gif": "photo",
		"image/webp": "photo",
		"image/bmp": "photo",
		"image/tiff": "photo",

		# Видео
		"video/mp4": "video",
		"video/mpeg": "video",
		"video/quicktime": "video",
		"video/x-msvideo": "video",
		"video/webm": "video",
		"video/ogg": "video",

		# Аудио
		"audio/mpeg": "audio",
		"audio/wav": "audio", 
		"audio/ogg": "audio",
		"audio/webm": "audio",
		"audio/aac": "audio",
		"audio/flac": "audio",

		# Документы
		"application/pdf": "document",
		"application/msword": "document",
		"application/vnd.openxmlformats-officedocument.wordprocessingml.document": "document",
		"application/vnd.ms-excel": "document",
		"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "document",
		"application/vnd.ms-powerpoint": "document",
		"application/vnd.openxmlformats-officedocument.presentationml.presentation": "document",
		"application/vnd.oasis.opendocument.text": "document",
		"application/vnd.oasis.opendocument.spreadsheet": "document",
		"application/vnd.oasis.opendocument.presentation": "document",
		"text/plain": "document",
		"text/csv": "document",
		"application/rtf": "document",
	}

	# Лимиты по категориям
	CATEGORY_LIMITS = {
		"photo": 10 * 1024 * 1024,		# 10MB
		"video": 500 * 1024 * 1024,		# 500MB
		"audio": 50 * 1024 * 1024,		# 50MB
		"document": 50 * 1024 * 1024,	# 50MB
	}

	@staticmethod
	async def validate_file(file: UploadFile) -> str:
		"""
		Валидирует файл и возвращает его категорию
		Возвращает: "photo", "video", "audio", "document"
		"""
		if not file.filename or not file.content_type:
			raise ValidateFileError(message="Файл должен иметь имя и MIME-тип")

		# Определяем категорию по MIME-type
		category = MediaFileValidator.MIME_TO_CATEGORY.get(file.content_type)
		if not category:
			raise ValidateFileError(message=f"Неподдерживаемый тип файла: {file.content_type}")

		# Проверяем размер
		max_size = MediaFileValidator.CATEGORY_LIMITS[category]
		await MediaFileValidator._check_size(file=file, max_size=max_size)

		return category

	@staticmethod
	async def _check_size(file: UploadFile, max_size: int) -> None:
		"""Проверка размера файла"""
		try:
			content = await file.read(max_size + 1)

			if len(content) > max_size:
				raise ValidateFileError(message=f"Превышен максимальный размер файла: {max_size // 1024 // 1024}MB")

		except ValidateFileError:
			raise

		except Exception as e:
			raise ValidateFileError(message="Ошибка при чтении файла")

		finally:
			await file.seek(0)
