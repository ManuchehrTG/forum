import logging
from typing import List
from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.media_files.commands import UploadFilesCommand
from src.domain.interfaces.file_validator import FileValidator
from src.domain.interfaces.storage_service import StorageService
from src.domain.media_files.entities import MediaFile
from src.domain.media_files.repository import MediaFileRepository

logger = logging.getLogger()

class UploadFiles:
	def __init__(self, media_file_repo: MediaFileRepository, file_validator: FileValidator, storage_service: StorageService):
		self.media_file_repo = media_file_repo
		self.file_validator = file_validator
		self.storage_service = storage_service

	@handle_domain_errors
	async def execute(self, command: UploadFilesCommand) -> List[UUID]:
		# На данный момент command.is_temp всегда True, т.к. для моей аппки пока-что только так и нужно.

		media_file_ids = []
		failed_files = []

		for file in command.files:
			try:
				# Валидация
				await self.file_validator.validate(file)

				path = await self.storage_service.save(file, is_temp=command.is_temp)

				media_file = MediaFile.create(
					author_id=command.author_id,
					filename=path.split("/")[-1],
					original_filename=file.filename,	# pyright: ignore[reportArgumentType]
					file_size=file.size,				# pyright: ignore[reportArgumentType]
					mime_type=file.content_type,		# pyright: ignore[reportArgumentType]
					storage_path=path,
					is_temp=command.is_temp
				)

				await self.media_file_repo.save(media_file)
				media_file_ids.append(media_file.id)
			except Exception as e:
				# Логируем ошибку, но продолжаем с другими файлами
				logger.error(f"Failed to upload file {file.filename}: {e}")
				failed_files.append({"filename": file.filename,"error": str(e)})

		if failed_files:
			logger.warning(f"Some files failed: {failed_files}")

		return media_file_ids
