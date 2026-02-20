from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field

class CreateMessageCommand(BaseModel):
	"""Команда для создания любого типа сообщения"""

	# Базовые поля для создания сообщения
	author_id: UUID
	theme_id: UUID
	section_id: UUID
	type: str
	text: str
	is_openai_generated: bool = False

	# Поля для конкретных типов
	ratio: int | None = None  # для task
	content_id: UUID | None = None  # для comment/task_assignment
	reply_to_message_id: UUID | None = None  # для comment
	assigned_to_user_id: UUID | None = None  # для task_assignment
	is_partially: bool = False  # для task_assignment
	expires_at: datetime | None = None  # для task_assignment


# ============ СПЕЦИАЛИЗИРОВАННЫЕ КОМАНДЫ ============

class BaseCreateMessageCommand(BaseModel):
	author_id: UUID
	theme_id: UUID
	section_id: UUID
	is_openai_generated: bool
	media_file_ids: List[UUID] = Field(default_factory=list)



class CreatePostCommand(BaseCreateMessageCommand):
	"""Команда создания поста"""
	text: str | None


class CreateTaskCommand(BaseCreateMessageCommand):
	"""Команда создания задачи"""
	text: str

	ratio: int


class CreateTaskAssignmentCommand(BaseCreateMessageCommand):
	"""Команда создания назначения задачи"""
	text: str

	content_id: UUID  # ID задачи, которую берем
	is_partially: bool
	expires_at: datetime


class CreateCommentCommand(BaseCreateMessageCommand):
	"""Команда создания комментария"""
	text: str | None

	content_id: UUID  # ID сообщения, к которому комментарий
	reply_to_message_id: UUID | None


# ============ ДРУГИЕ КОМАНДЫ ============

@dataclass
class UpdateMessageCommand:
	"""Команда обновления сообщения"""
	message_id: UUID
	text: str


@dataclass
class DeleteMessageCommand:
	"""Команда удаления сообщения"""
	message_id: UUID
	deleted_by: UUID  # Кто удалил


@dataclass
class AssignTaskCommand:
	"""Команда назначения задачи пользователю"""
	task_assignment_id: UUID
	user_id: UUID


@dataclass
class CompleteTaskCommand:
	"""Команда завершения задачи"""
	task_assignment_id: UUID
	completed_by: UUID
	notes: str | None = None
