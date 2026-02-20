from typing import List

from src.application.decorators import handle_domain_errors
from src.application.media_files.dtos import MediaFileDTO
from src.application.media_files.queries import GetFilesQuery
from src.domain.media_files.entities import MediaFile
from src.domain.media_files.repository import MediaFileRepository
from src.domain.interfaces.storage_service import StorageService

class GetFiles:
	def __init__(self, media_file_repo: MediaFileRepository, storage_service: StorageService):
		self.media_file_repo = media_file_repo
		self.storage_service = storage_service

	@handle_domain_errors
	async def execute(self, query: GetFilesQuery) -> List[MediaFileDTO]:
		media_files = await self.media_file_repo.get_many_by_ids(query.media_file_ids)
		return [self._to_dto(mf) for mf in media_files]

	def _to_dto(self, media_file: MediaFile) -> MediaFileDTO:
		return MediaFileDTO(
			id=media_file.id,
			author_id=media_file.author_id,
			filename=media_file.filename,
			original_filename=media_file.original_filename,
			file_size=media_file.file_size,
			mime_type=media_file.mime_type,
			extension=media_file.extension,
			is_temp=media_file.is_temp,
			url=self.storage_service.get_url(media_file.storage_path),
			created_at=media_file.created_at,
			updated_at=media_file.updated_at,
		)
