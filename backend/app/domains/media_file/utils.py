import aiofiles
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import List
from uuid import uuid4

from app.core.config import settings
from app.utils.logger import logger
from .schemas import MediaFile

class MediaFileUtils:
	@staticmethod
	def generate_filename(original_name: str) -> str:
		"""Генерация уникального имени файла с сохранением расширения"""

		ext = Path(original_name).suffix.lower()
		return f"{uuid4().hex}{ext}"

	@staticmethod
	async def save_to_disk(file: UploadFile, file_path: Path) -> None:
		"""Асинхронное сохранение файла на диск"""
		file_path.parent.mkdir(parents=True, exist_ok=True)

		content = await file.read()
		async with aiofiles.open(file_path, "wb") as buffer:
			await buffer.write(content)

		await file.seek(0)

	@staticmethod
	def move_temp_files_to_permanent_storage(files: List[MediaFile]):
		storage_dir_path = Path(settings.STORAGE_DIR)

		for file in files:
			# logger.info(f"Processing file ID: {file.id}")
			# logger.info(f"Original file_path: {file.file_path}")
			# logger.info(f"Filename from path: {Path(file.file_path).name}")

			current_relative_path = Path(file.file_path)
			current_full_path = storage_dir_path / current_relative_path

			if current_relative_path.parts[0] != "temp":
				raise ValueError(f"File {file.file_path} is not in temp directory")

			new_relative_path = Path(*current_relative_path.parts[1:])
			new_full_path = storage_dir_path / new_relative_path

			# logger.info(f"Moving from: {current_full_path}")
			# logger.info(f"Moving to: {new_full_path}")

			new_full_path.parent.mkdir(parents=True, exist_ok=True)
			shutil.move(str(current_full_path), str(new_full_path))

			file.file_path = new_relative_path.as_posix()

			# logger.info(f"Moved file from {current_full_path} to {new_full_path}")

		return files
