from datetime import datetime, timedelta
from fastapi import UploadFile
from fastapi.responses import FileResponse
from pathlib import Path
from typing import List
from uuid import UUID

from app.core.config import settings
from app.domains.user.schemas import User
from .repositories import MediaFileRepository
from .exceptions import MediaFileError, ValidateFileError, MediaFilesExpiredError
from .schemas import MediaFile, MediaFileCreateData, MediaFileStatusType
from .utils import MediaFileUtils
from .validator import MediaFileValidator

class MediaFileService:
	async def save_uploaded_file(self, file: UploadFile, user: User, upload_subdir: str, is_temp: bool) -> MediaFile:
		try:
			# Валидация
			file_type = await MediaFileValidator.validate_file(file=file)

			storage_dir_path = Path(settings.STORAGE_DIR)

			if is_temp:
				upload_dir_path = storage_dir_path / "temp" / upload_subdir
			else:
				upload_dir_path = storage_dir_path / upload_subdir

			upload_dir_path.mkdir(parents=True, exist_ok=True)

			# Генерация имени и сохранение
			new_filename = MediaFileUtils.generate_filename(original_name=file.filename)
			file_path = upload_dir_path / new_filename

			await MediaFileUtils.save_to_disk(file=file, file_path=file_path)

			relative_path = file_path.relative_to(storage_dir_path).as_posix()

			metadata = {}
			# if file_type in ("image", "video"):
			# 	metadata = await MediaUtils.extract_metadata(file_path=file_path)

			expires_at = datetime.now() + timedelta(minutes=60) if is_temp else None

			media_file_data = MediaFileCreateData(
				author_id=user.id,
				file_path=relative_path,
				original_name=file.filename,
				mime_type=file.content_type,
				file_size=file.size,
				status="temporary" if is_temp else "attached",
				metadata=metadata,
				expires_at=expires_at
			)

			return await MediaFileRepository.create_media_file(data=media_file_data)

		except ValidateFileError:
			raise

		except Exception as e:
			# logger.error(f"Error `save_uploaded_file` for {file.filename}", exc_info=True)
			raise MediaFileError(
				message=f"Could not process file {file.filename}",
				original_error=str(e),
				file_name=file.filename
			)

	async def save_files(self, files: List[UploadFile], user: User, upload_subdir: str, is_temp: bool = False) -> List[MediaFile]:
		return [
			await self.save_uploaded_file(file=file, user=user, upload_subdir=upload_subdir, is_temp=is_temp)
			for file in files
		]

	async def get_temporary_media_files_by_ids(self, media_file_ids: List[UUID]) -> List[MediaFile]:
		return await MediaFileRepository.get_temporary_media_files_by_ids(media_file_ids=media_file_ids)

	async def activate_media_files(self, media_files: List[MediaFile]) -> List[MediaFile]:
		try:
			media_files = MediaFileUtils.move_temp_files_to_permanent_storage(files=media_files)
		except ValueError as e:
			logger.error(e, exp_info=True)
			raise MediaFilesExpiredError(message="Temporary upload file(s) have expired")

		return [
			await MediaFileRepository.activate_media_file(media_file=media_file)
			for media_file in media_files
		]

	async def get_media_files_by_ids(self, media_file_ids: List[UUID]) -> List[MediaFile]:
		return await MediaFileRepository.get_media_files_by_ids(media_file_ids=media_file_ids)


	# async def download_file(url: str, subdir: str | None):
	# 	storage_path = Path(settings.STORAGE_DIR).absolute()

	# 	if subdir:
	# 		file_path = storage_path / subdir / url
	# 	else:
	# 		file_path = storage_path / url

	# 	if not file_path.exists():
	# 		raise _FileNotFoundError()

	# 	return FileResponse(file_path)
