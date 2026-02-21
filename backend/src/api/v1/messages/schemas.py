from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Dict, List
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

class MessageReactionTypeAPI(str, Enum):
	LIKE = "like"
	DISLIKE = "dislike"


class MessageMediaFileData(BaseModel):
	media_file_id: UUID = Field(..., description="ID медиафайла")
	sort_order: int = Field(..., description="Сортировка по возростанию")

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

class MessageBaseResponse(BaseModel):
	"""Базовая схема ответа"""
	id: UUID = Field(..., description="ID сообщения")
	type: MessageTypeAPI = Field(..., description="Тип сообщения")
	text: str | None = Field(None, description="Текст сообщения. Может быть пустым.")
	author_id: UUID = Field(..., description="ID автора")
	theme_id: UUID = Field(..., description="ID темы")
	section_id: UUID = Field(..., description="ID секции")
	is_openai_generated: bool = Field(False, description="Сгенерировано ли с помощью AI")
	created_at: datetime = Field(..., description="Дата создания")
	updated_at: datetime = Field(..., description="Дата обновления")

	media_files: List[MessageMediaFileData] = Field(..., description="Медиафайлы")

class PostMessageResponse(MessageBaseResponse):
	"""Ответ с данными поста"""
	pass

class TaskMessageResponse(MessageBaseResponse):
	"""Ответ с данными задачи"""
	ratio: int = Field(..., description="Коэффициент задачи")

class TaskAssignmentResponse(MessageBaseResponse):
	"""Ответ с данными назначения задачи"""
	content_id: UUID = Field(..., description="ID сообщения, к которому комментарий")
	is_partially: bool = Field(False, description="Частично")
	status: str = Field(..., description="Статус")
	expires_at: datetime = Field(..., description="Дата дедлайна")

class CommentMessageResponse(MessageBaseResponse):
	"""Ответ с данными комментария"""
	content_id: UUID = Field(..., description="ID сообщения, к которому комментарий")
	reply_to_message_id: UUID | None = Field(None, description="ID комментария, на который отвечаем")

# Union для общего ответа
MessageResponse = MessageBaseResponse | TaskMessageResponse | CommentMessageResponse | TaskAssignmentResponse



class UpsertMessageReactionRequest(BaseModel):
	reaction: MessageReactionTypeAPI | None = Field(..., description="Реакция для сообщения. None чтобы удалить")

class MessageReactionResponse(BaseModel):
	user_id: UUID = Field(..., description="ID пользователя")
	message_id: UUID = Field(..., description="ID сообщения")
	reaction: MessageReactionTypeAPI = Field(..., description="Реакция текущего пользователя")
	updated_at: datetime = Field(..., description="Дата обновления")

class MessageReactionStatsResponse(BaseModel):
	reactions: Dict[MessageReactionTypeAPI, int] = Field(default_factory=dict, description="Все реакции сообщения. <reaction>: <count>")
	total: int = Field(..., description="Количество реакций")
