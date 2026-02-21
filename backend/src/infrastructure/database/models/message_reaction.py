import uuid
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base, TimestampMixin

class MessageReactionModel(Base, TimestampMixin):
	__tablename__ = "message_reactions"

	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
	reaction: Mapped[str] = mapped_column(String(32), nullable=False)

	__table_args__ = (UniqueConstraint("user_id", "message_id"),)
