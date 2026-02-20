import aiofiles
from datetime import UTC, datetime
from fastapi import UploadFile
from pathlib import Path
from uuid import uuid4

from src.domain.interfaces.storage_service import StorageService

class LocalStorageService(StorageService):
	"""Адаптер для локальной файловой системы"""

	def __init__(self, base_path: Path, base_url: str): # Непонятно что за base_path и base_url
		self.base_path = base_path
		self.base_url = base_url.rstrip("/")

		# Создаем структуру папок
		self.temp_path = base_path / "temp"
		self.permanent_path = base_path / "permanent"
		self.temp_path.mkdir(parents=True, exist_ok=True)
		self.permanent_path.mkdir(parents=True, exist_ok=True)

	async def save(self, file: UploadFile, is_temp: bool = True, custom_path: str | None = None) -> str:
		"""Сохранить файл"""
		if custom_path:
			relative_path = custom_path
		else:
			# Генерируем путь: temp/2026/02/13/uuid.ext
			date_path = datetime.now(UTC).strftime("%Y/%m/%d")
			ext = file.filename.split(".")[-1] # pyright: ignore[reportOptionalMemberAccess]
			filename = f"{uuid4()}.{ext}"

			folder = "temp" if is_temp else "permanent"
			relative_path = f"{folder}/{date_path}/{filename}"

		full_path = self.base_path / relative_path
		full_path.parent.mkdir(parents=True, exist_ok=True)

		# Сохраняем файл
		async with aiofiles.open(full_path, "wb") as f:
			content = await file.read()
			await f.write(content)

		return relative_path

	def delete(self, path: str) -> bool:
		"""Удалить файл"""
		full_path = self.base_path / path
		if full_path.exists():
			full_path.unlink()
			return True
		return False

	def get_url(self, path: str) -> str:
		"""Получить URL"""
		return f"{self.base_url}/{path}"

	def move(self, source_path: str, new_path: str) -> None:
		"""
		Универсальный метод перемещения

		Args:
			source_path: исходный путь (например "temp/2026/02/14/file.jpg")
			new_path: куда перемещаем (messages/<UUID>/file.jpg, avatars/<UUID>/photo.png, ...)

		Returns:
			новый относительный путь
		"""
		source_full = self.base_path / source_path

		if not source_full.exists():
			raise FileNotFoundError(f"Source file not found: {source_path}")

		target_full = self.base_path / new_path
		target_full.parent.mkdir(parents=True, exist_ok=True)

		# Перемещаем файл
		source_full.rename(target_full)
