from datetime import datetime
from typing import Optional
import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func, text as sqlalchemy_text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import Base, TimestampMixin

class MessageModel(Base, TimestampMixin):
	__tablename__ = "messages"

	author_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
	theme_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("themes.id", ondelete="CASCADE"), nullable=False)
	section_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sections.id", ondelete="CASCADE"), nullable=False)
	type: Mapped[str] = mapped_column(String(32), nullable=False)
	text: Mapped[str | None] = mapped_column(Text, nullable=True)
	is_openai_generated: Mapped[bool] = mapped_column(Boolean, server_default=sqlalchemy_text("true"))

	# Relationships для специфичных данных
	post_data: Mapped[Optional["PostMessageData"]] = relationship(back_populates="message", cascade="all, delete-orphan")
	task_data: Mapped[Optional["TaskMessageData"]] = relationship(back_populates="message", cascade="all, delete-orphan")
	comment_data: Mapped[Optional["CommentMessageData"]] = relationship(back_populates="message", cascade="all, delete-orphan")
	task_assignment_data: Mapped[Optional["TaskAssignmentMessageData"]] = relationship(back_populates="message", cascade="all, delete-orphan")


class PostMessageData(Base):
	__tablename__ = "post_message_data"

	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), unique=True, nullable=False)

	message: Mapped["MessageModel"] = relationship(back_populates="post_data")


class TaskMessageData(Base):
	__tablename__ = "task_message_data"

	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), unique=True, nullable=False)

	ratio: Mapped[int] = mapped_column(Integer, nullable=False)

	message: Mapped["MessageModel"] = relationship(back_populates="task_data")


class TaskAssignmentMessageData(Base):
	__tablename__ = "task_assignment_message_data"

	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), unique=True, nullable=False)

	content_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
	is_partially: Mapped[bool] = mapped_column(Boolean, server_default=sqlalchemy_text("false"))
	status: Mapped[str] = mapped_column(String(16), nullable=False)
	expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

	message: Mapped["MessageModel"] = relationship(back_populates="task_assignment_data")
	task_message: Mapped["MessageModel"] = relationship(foreign_keys=[content_id], backref="assignments")


class CommentMessageData(Base):
	__tablename__ = "comment_message_data"

	message_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), unique=True, nullable=False)

	content_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
	reply_to_message_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)

	message: Mapped["MessageModel"] = relationship(back_populates="comment_data")
	content: Mapped["MessageModel"] = relationship(foreign_keys=[content_id], backref="comments_on_content")
	reply_to: Mapped[Optional["MessageModel"]] = relationship(foreign_keys=[reply_to_message_id])
