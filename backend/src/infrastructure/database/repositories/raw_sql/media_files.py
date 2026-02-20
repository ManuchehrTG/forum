from asyncpg import Pool
from typing import List
from uuid import UUID

from src.domain.media_files.entities import MediaFile
from src.domain.media_files.repository import MediaFileRepository

class RawSQLMediaFileRepository(MediaFileRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def save(self, media_file: MediaFile) -> None:
		async with self.pool.acquire() as connection:
			await connection.execute(
				"""
				INSERT INTO media_files (id, author_id, filename, original_filename, file_size, mime_type, extension, extra, storage_path, is_temp, created_at, updated_at)
				VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
				ON CONFLICT (id) DO UPDATE SET
					filename = EXCLUDED.filename,
					file_size = EXCLUDED.file_size,
					mime_type = EXCLUDED.mime_type,
					extension = EXCLUDED.extension,
					extra = EXCLUDED.extra,
					storage_path = EXCLUDED.storage_path,
					is_temp = EXCLUDED.is_temp,
					updated_at = EXCLUDED.updated_at
				""",
				media_file.id, media_file.author_id, media_file.filename, media_file.original_filename, media_file.file_size, media_file.mime_type, media_file.extension,
				media_file.metadata, media_file.storage_path, media_file.is_temp, media_file.created_at, media_file.updated_at
			)

	async def save_many(self, media_files: List[MediaFile]) -> None:
		async with self.pool.acquire() as connection:
			params = [
				(
					media_file.id,
					media_file.author_id,
					media_file.filename,
					media_file.original_filename,
					media_file.file_size,
					media_file.mime_type,
					media_file.extension,
					media_file.metadata,
					media_file.storage_path,
					media_file.is_temp,
					media_file.created_at,
					media_file.updated_at
				)
				for media_file in media_files
			]

			await connection.executemany(
				"""
				INSERT INTO media_files (id, author_id, filename, original_filename, file_size, mime_type, extension, extra, storage_path, is_temp, created_at, updated_at)
				VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
				ON CONFLICT (id) DO UPDATE SET
					filename = EXCLUDED.filename,
					file_size = EXCLUDED.file_size,
					mime_type = EXCLUDED.mime_type,
					extension = EXCLUDED.extension,
					extra = EXCLUDED.extra,
					storage_path = EXCLUDED.storage_path,
					is_temp = EXCLUDED.is_temp,
					updated_at = EXCLUDED.updated_at
				""",
				params
			)

	async def get_many_by_ids(self, media_file_ids: List[UUID]) -> List[MediaFile]:
		async with self.pool.acquire() as connection:
			rows = await connection.fetch("SELECT * FROM media_files WHERE id = ANY($1)", media_file_ids)
			return [MediaFile.from_db_record(row) for row in rows]
