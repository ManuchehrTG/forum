import uuid
from sqlalchemy import BigInteger, Boolean, ForeignKey, String, Index, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class MediaFileModel(Base, TimestampMixin):
	"""
	Модель для хранения информации о медиафайлах.
	Агрегат - файл существует независимо от сообщений.
	"""
	__tablename__ = "media_files"

	author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)

	# Основная информация о файле
	filename: Mapped[str] = mapped_column(String(255), nullable=False)
	original_filename: Mapped[str] = mapped_column(String(255), nullable=False)
	file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)  # в байтах
	mime_type: Mapped[str] = mapped_column(String(127), nullable=False)
	extension: Mapped[str] = mapped_column(String(50), nullable=False)
	extra: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb")) # metadata

	# Хранение файла
	storage_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)  # путь в S3/локальном хранилище

	is_temp: Mapped[bool] = mapped_column(Boolean, server_default=text("true"), index=True)

	__table_args__ = (
		Index("ix_media_files_author_id", "author_id"),
		Index("ix_media_files_is_temp", "is_temp"),
	)
