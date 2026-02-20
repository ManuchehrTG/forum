import uuid
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base

class SectionMessageTypeModel(Base):
	__tablename__ = "section_message_types"

	section_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
	message_type: Mapped[str] = mapped_column(String(32), nullable=False)
	allow_comments: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

	__table_args__ = (UniqueConstraint("section_id", "message_type"),)

	# section: Mapped["SectionModel"] = relationship(back_populates="allowed_message_types")
