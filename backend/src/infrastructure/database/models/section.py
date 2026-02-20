from sqlalchemy import Boolean, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class SectionModel(Base, TimestampMixin):
	__tablename__ = "sections"

	code: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
	openai_prompt: Mapped[str | None] = mapped_column(Text, nullable=True)
	tech_version: Mapped[str] = mapped_column(Text, nullable=False)
	enable_openai: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))
	allow_hide: Mapped[bool] = mapped_column(Boolean, server_default=text("true"))

	# allowed_message_types: Mapped[List["SectionMessageTypeModel"]] = relationship(
	# 	back_populates="section", 
	# 	cascade="all, delete-orphan"
	# )
