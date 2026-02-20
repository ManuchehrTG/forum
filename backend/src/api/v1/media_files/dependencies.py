from asyncpg import Pool
from fastapi import Depends
from typing import List
from uuid import UUID

from src.api.dependencies import get_db_pool
from src.application.media_files.queries import GetFilesQuery
from src.application.media_files.use_cases.get_files import GetFiles
from src.application.media_files.use_cases.upload_files import UploadFiles
from src.domain.interfaces.file_validator import FileValidator
from src.domain.interfaces.storage_service import StorageService
from src.domain.media_files.repository import MediaFileRepository
from src.infrastructure.database.repositories.raw_sql.media_files import RawSQLMediaFileRepository
from src.infrastructure.services.validation.factory import create_file_validator
from src.infrastructure.services.storage.factory import create_storage_service

async def get_media_file_repository(
	pool: Pool = Depends(get_db_pool)
) -> MediaFileRepository:
	return RawSQLMediaFileRepository(pool)

async def get_file_validator():
	return create_file_validator()

async def get_storage_service():
	return create_storage_service()

async def get_upload_files(
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	file_validator: FileValidator = Depends(get_file_validator),
	storage_service: StorageService = Depends(get_storage_service)
):
	return UploadFiles(media_file_repo, file_validator=file_validator, storage_service=storage_service)


async def get_retrieve_media_files(
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	storage_service: StorageService = Depends(get_storage_service)
) -> GetFiles:
	return GetFiles(media_file_repo, storage_service)

async def get_media_files(
	media_file_ids: List[UUID],
	get_files: GetFiles = Depends(get_retrieve_media_files)
):
	query = GetFilesQuery(media_file_ids=media_file_ids)
	return await get_files.execute(query)
