from typing import Any, List
from uuid import UUID

from infrastructure.database import db
from .schemas import MediaFile, MediaFileCreateData, MediaFileStatusType

class MediaFileRepository:
	@staticmethod
	async def create_media_file(data: MediaFileCreateData) -> MediaFile:
		record = await db.fetchrow(
			"""
			INSERT INTO media_files (author_id, file_path, original_name, mime_type, file_size, status, expires_at)
			VALUES ($1, $2, $3, $4, $5, $6, $7)
			RETURNING *
			""",
			data.author_id,
			data.file_path,
			data.original_name,
			data.mime_type,
			data.file_size,
			data.status,
			data.expires_at
		)

		return MediaFile(**record)

	@staticmethod
	async def get_temporary_media_files_by_ids(media_file_ids: List[UUID]) -> List[MediaFile]:
		records = await db.fetch(
			"""
			SELECT *
			FROM media_files
			WHERE
				id = ANY($1) AND
				status = $2 AND
				now() < expires_at
			""",
			media_file_ids, MediaFileStatusType.TEMPORARY
		)
		return [MediaFile(**record) for record in records]

	@staticmethod
	async def activate_media_file(media_file: MediaFile) -> MediaFile:
		record = await db.fetchrow(
			"""
			UPDATE media_files
			SET file_path = $1, status = 'attached', expires_at = NULL
			WHERE id = $2
			RETURNING *
			""",
			media_file.file_path, media_file.id
		)
		return MediaFile(**record)

	@staticmethod
	async def get_media_files_by_ids(media_file_ids: List[UUID]) -> List[MediaFile]:
		records = await db.fetch("SELECT * FROM media_files WHERE id = ANY($1)", media_file_ids)
		return [MediaFile(**record) for record in records]

	# @staticmethod
	# async def get_by_message_attachments(message_id: int):
	# 	return await db.fetch(
	# 		"""
	# 		SELECT
	# 			mf.*
	# 		FROM media_files mf
	# 		JOIN message_attachments ma ON mf.id = ma.attachment_id
	# 		WHERE ma.message_id = $1
	# 		ORDER BY ma.sort_order ASC
	# 		""",
	# 		message_id
	# 	)
