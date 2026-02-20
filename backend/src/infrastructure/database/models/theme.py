import uuid
from sqlalchemy import Boolean, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class ThemeModel(Base, TimestampMixin):
	__tablename__ = "themes"

	parent_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("themes.id", ondelete="SET NULL"), nullable=True)
	author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=False)
	title: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
	is_group: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
