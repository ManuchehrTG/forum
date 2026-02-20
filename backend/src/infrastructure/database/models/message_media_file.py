import uuid
from sqlalchemy import ForeignKey, Integer, Index, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base

class MessageMediaFileModel(Base):
	"""
	Модель для связи сообщений с медиафайлами.
	Содержит информацию о конкретном использовании файла в сообщении.
	"""
	__tablename__ = "message_media_files"

	# Связи
	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
	media_file_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("media_files.id", ondelete="CASCADE"), nullable=False)

	# Порядок отображения
	sort_order: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

	# is_cover: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

	# Связи
	message: Mapped["MessageModel"] = relationship(back_populates="media_files")
	media_file: Mapped["MediaFileModel"] = relationship(back_populates="messages")

	__table_args__ = (
		UniqueConstraint("message_id", "media_file_id"),
		Index("ix_message_media_message_id", "message_id"),
		Index("ix_message_media_media_file_id", "media_file_id"),
	)
