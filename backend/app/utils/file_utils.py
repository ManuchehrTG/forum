import aiofiles
import os
from fastapi import UploadFile
from uuid import uuid4

class FileUtils:
	@staticmethod
	def generate_filename(original_name: str) -> str:
		"""Генерация уникального имени файла с сохранением расширения"""
		ext = os.path.splitext(original_name)[1].lower()
		return f"{uuid4().hex}{ext}"

	@staticmethod
	async def save_to_disk(file: UploadFile, path: str) -> None:
		"""Асинхронное сохранение файла на диск"""
		os.makedirs(os.path.dirname(path), exist_ok=True)
		async with aiofiles.open(path, "wb") as buffer:
			await buffer.write(await file.read())
