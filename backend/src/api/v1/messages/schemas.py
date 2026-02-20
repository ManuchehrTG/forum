from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import List
from uuid import UUID

class MessageTypeAPI(str, Enum):
    POST = "post"
    TASK = "task"
    TASK_ASSIGNMENT = "task_assignment"
    COMMENT = "comment"

class TaskMessageStatusAPI(str, Enum):
	IN_PROGRESS = "in_progress"
	COMPLETED = "completed"
	CANCELLED = "cancelled"
	FAILED = "failed"

# ============ REQUEST SCHEMAS ============

class BaseMessageRequest(BaseModel):
	"""Базовая схема для всех сообщений"""
	text: str | None = Field(None, description="Текст сообщения. Может быть пустым.")
	is_openai_generated: bool = Field(False, description="Сгенерировано ли с помощью AI")
	media_file_ids: List[UUID] = Field(default_factory=list, description="ID медиафайлов, которые нужно прикрепить")

	@field_validator("text")
	@classmethod
	def validate_text(cls, v) -> str | None:
		if v is None:
			return

		if not v.strip():
			raise ValueError("Text cannot be empty")
		return v.strip()

class CreatePostRequest(BaseMessageRequest):
	"""Создание обычного поста"""
	pass

class CreateTaskRequest(BaseMessageRequest):
	"""Создание задачи"""
	ratio: int = Field(..., ge=1, le=100, description="Коэффициент задачи (1-100)")

class CreateTaskAssignmentRequest(BaseMessageRequest):
	"""Взятие задачи в работу"""
	expires_at: datetime = Field(..., description="Дедлайн")
	is_partially: bool = Field(False, description="Частично")

class CreateCommentRequest(BaseMessageRequest):
	"""Создание комментария"""
	reply_to_message_id: UUID | None = Field(None, description="ID комментария, на который отвечаем")

# Union для общего эндпоинта
CreateMessageRequest = CreatePostRequest | CreateTaskRequest | CreateTaskAssignmentRequest | CreateCommentRequest

# ============ RESPONSE SCHEMAS ============

class MessageMediaFileRepsonse(BaseModel):
	media_file_id: UUID
	sort_order: int

class MessageBaseResponse(BaseModel):
	"""Базовая схема ответа"""
	id: UUID
	type: MessageTypeAPI
	text: str
	author_id: UUID | None
	theme_id: UUID
	section_id: UUID
	is_openai_generated: bool
	created_at: datetime
	updated_at: datetime

	media_files: List[MessageMediaFileRepsonse]

class PostMessageResponse(MessageBaseResponse):
	"""Ответ с данными поста"""
	pass

class TaskMessageResponse(MessageBaseResponse):
	"""Ответ с данными задачи"""
	ratio: int

class TaskAssignmentResponse(MessageBaseResponse):
	"""Ответ с данными назначения задачи"""
	content_id: UUID = Field(..., description="ID сообщения, к которому комментарий")
	is_partially: bool
	status: str
	expires_at: datetime

class CommentMessageResponse(MessageBaseResponse):
	"""Ответ с данными комментария"""
	content_id: UUID = Field(..., description="ID сообщения, к которому комментарий")
	reply_to_message_id: UUID | None

# Union для общего ответа
MessageResponse = MessageBaseResponse | TaskMessageResponse | CommentMessageResponse | TaskAssignmentResponse


# ============ SPECIAL RESPONSES ============

class MessageCreatedResponse(BaseModel):
	"""Минимальный ответ после создания"""
	id: UUID
	created_at: datetime
