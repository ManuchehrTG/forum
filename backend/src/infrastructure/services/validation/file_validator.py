from fastapi import UploadFile
from pydantic import ValidationError
from typing import List

from src.domain.interfaces.file_validator import FileValidator

class DefaultFileValidator(FileValidator):
	def __init__(
		self,
		max_size: int = 100 * 1024 * 1024,  # 100MB
		allowed_types: List[str] | None = None,
		allowed_extensions: List[str] | None = None
	):
		self.max_size = max_size
		self.allowed_types = allowed_types or [
			"image/jpeg", "image/png", "image/gif",
			"video/mp4", "video/quicktime",
			"application/pdf"
		]
		self.allowed_extensions = allowed_extensions or [
			"jpg", "jpeg", "png", "gif", "mp4", "mov", "pdf"
		]

	async def validate(self, file: UploadFile) -> bool:
		"""Валидация файла"""

		# 1. Базовая проверка наличия данных
		await self._validate_basic(file)

		# 2. Проверка имени файла
		self._validate_filename(file.filename) # pyright: ignore[reportArgumentType]

		# 3. Проверка расширения
		self._validate_extension(file.filename) # pyright: ignore[reportArgumentType]

		# 4. Проверка MIME type
		await self._validate_mime_type(file)

		return True

	async def _validate_basic(self, file: UploadFile):
		"""Базовая проверка наличия данных"""

		# Проверка что файл не пустой:
		if not file:
			raise ValidationError("File is empty or None")

		# Проверка что есть имя
		if not file.filename:
			raise ValidationError("Filename is missing")

		# Проверка что размер существует
		if file.size is None:
			raise ValidationError(f"File size is unknown")

		# Проверка размера
		if file.size and file.size > self.max_size:
			raise ValidationError(f"File too large: {file.size} > {self.max_size}")

		# Проверка что есть content type
		if not file.content_type:
			raise ValidationError("Content type is missing")

	def _validate_filename(self, filename: str):
		"""Проверка имени файла на корректность"""

		if len(filename) > 255:
			raise ValidationError(f"Filename too long: {len(filename)} > 255")

		# Пустое имя после очистки
		if not filename.strip():
			raise ValidationError("Filename is empty after stripping")

		# Запрещенные символы (path traversal)
		forbidden = ["..", "/", "\\", "%00", "\x00"]
		for char in forbidden:
			if char in filename:
				raise ValidationError(f"Filename contains forbidden character: {char}")

		# Пустое имя после очистки
		if not filename.strip():
			raise ValidationError("Filename is empty after stripping")

		# Скрытые файлы (опционально)
		if filename.startswith("."):
			raise ValidationError("Hidden files are not allowed")

	def _validate_extension(self, filename: str):
		"""Проверка расширения файла"""

		# Нет расширения
		if "." not in filename:
			raise ValidationError("File has no extension")

		ext = filename.split(".")[-1].lower()

		# Пустое расширение
		if not ext:
			raise ValidationError("Empty file extension")

		# Проверка длины расширения
		if len(ext) > 10:
			raise ValidationError(f"Extension too long: {ext}")

		# Проверка что расширение разрешено
		if ext not in self.allowed_extensions:
			raise ValidationError(f"Invalid extension: {ext}")

		# Двойное расширение (потенциально опасное)
		if filename.count(".") > 2:
			raise ValidationError("Multiple extensions detected")

	async def _validate_mime_type(self, file: UploadFile):
		"""Проверка MIME type"""

		# Проверка что MIME type разрешен
		if file.content_type not in self.allowed_types:
			raise ValidationError(f"Invalid MIME type: {file.content_type}")

		# Специфичные проверки для разных типов
		if file.content_type.startswith("image/"):
			# Для изображений можно проверить максимальные размеры
			if file.content_type not in ["image/jpeg", "image/png", "image/gif", "image/webp"]:
				raise ValidationError(f"Unsupported image format: {file.content_type}")


	# async def validate_batch(self, files: List[UploadFile]) -> List[ValidationResult]:
	# 	"""Валидация нескольких файлов с детальным результатом"""
	# 	results = []

	# 	for file in files:
	# 		try:
	# 			await self.validate(file)
	# 			results.append(ValidationResult(
	# 				filename=file.filename,
	# 				success=True,
	# 				size=file.size
	# 			))
	# 		except ValidationError as e:
	# 			results.append(ValidationResult(
	# 				filename=file.filename,
	# 				success=False,
	# 				error=str(e)
	# 			))

	# 	return results
