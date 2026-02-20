import json
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.domain.media_files.exceptions import MediaFileStateConflictError

class MediaFile:
	"""Сущность MediaFile"""
	def __init__(
		self,
		id: UUID,
		author_id: UUID,
		filename: str,
		original_filename: str,
		file_size: int,
		mime_type: str,
		extension: str,
		storage_path: str,
		extra: dict | None = None,
		is_temp: bool = True,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
	):
		self.id = id
		self.author_id = author_id
		self.filename = filename
		self.original_filename = original_filename
		self.file_size = file_size
		self.mime_type = mime_type
		self.extension = extension
		self.extra = extra or {}
		self.storage_path = storage_path
		self.is_temp = is_temp

		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	@property
	def metadata(self):
		return json.dumps(self.extra, ensure_ascii=False)

	def _touch(self):
		self.updated_at = datetime.utcnow()

	def ensure_author(self, author_id: UUID):
		if self.author_id != author_id:
			PermissionError(f"MediaFile {self.id} belongs to another user")

	def ensure_is_temp(self):
		if not self.is_temp:
			raise MediaFileStateConflictError.incorrect_is_temp(self.id)

	@classmethod
	def create(cls, author_id: UUID, filename: str, original_filename: str, file_size: int, mime_type: str, storage_path: str, is_temp: bool = True) -> "MediaFile":
		extension = filename.split(".")[-1] if "." in filename else ""

		return cls(
			id=uuid4(),
            author_id=author_id,
            filename=filename,
            original_filename=original_filename,
            file_size=file_size,
            mime_type=mime_type,
            extension=extension,
            storage_path=storage_path,
            is_temp=is_temp,
		)

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			author_id=record["author_id"],
			filename=record["filename"],
			original_filename=record["original_filename"],
			file_size=record["file_size"],
			mime_type=record["mime_type"],
			extension=record["extension"],
			extra=json.loads(record["extra"]) if record["extra"] else {},
			storage_path=record["storage_path"],
			is_temp=record["is_temp"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	def promote(self, new_path: str):
		"""Перевести файл в постоянное хранение"""
		self.storage_path = new_path
		self.is_temp = False
		self.extra["promoted_at"] = datetime.now(UTC).isoformat()

		self._touch()
