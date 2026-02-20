import uuid
from sqlalchemy import Boolean, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base

class ThemeSectionModel(Base):
	__tablename__ = "theme_sections"

	theme_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
	section_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
	is_visible: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

	__table_args__ = (UniqueConstraint("theme_id", "section_id"),)
