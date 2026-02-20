import uuid
from sqlalchemy import ForeignKey, Text, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class LinkedAccountModel(Base, TimestampMixin):
	__tablename__ = "linked_accounts"

	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	provider: Mapped[str] = mapped_column(Text, nullable=False)
	provider_user_id: Mapped[str | None] = mapped_column(Text, nullable=True)
	extra: Mapped[dict] = mapped_column(JSONB, server_default=text("'{}'::jsonb"))

	__table_args__ = (UniqueConstraint("user_id", "provider"),)
