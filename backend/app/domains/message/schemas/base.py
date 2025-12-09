from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, field_validator
from uuid import UUID

class MessageType(str, Enum):
	MESSAGE = "message"
	POST = "post"
	COMMENT = "comment"
	TASK = "task" 

class MessageBase(BaseModel):
	type: MessageType = Field(..., description="Тип сообщения")
	text: str | None = Field(None, description="Текст сообщения")
	media_file_ids: List[UUID] = Field(default_factory=list, description="ID медиафайлов")

	@field_validator("text")
	@classmethod
	def validate_text_not_empty(cls, v: str | None) -> str | None:
		if v is not None and not v.strip():
			raise ValueError("Message text cannot be empty")
		return v.strip() if v else v

class Message(BaseModel):
	id: int = Field(..., description="ID сообщения")
	author_id: UUID = Field(..., description="ID автора")
	theme_id: int = Field(..., description="ID темы")
	section_code: str = Field(..., description="Раздел/секция")
	text: str | None = Field(..., description="Текст сообщения")
	type: MessageType = Field(..., description="Тип сообщения")
	created_at: datetime = Field(..., description="Дата создания")
	updated_at: datetime = Field(..., description="Дата обновления/изменения")

class MessageResponse(Message):
	pass
	# id: int = Field(..., description="ID сообщения")
	# author_id: UUID = Field(..., description="ID автора")
	# text: str | None = Field(..., description="Текст сообщения")
	# created_at: datetime = Field(..., description="Дата создания")
	# updated_at: datetime = Field(..., description="Дата обновления/изменения")

	# reactions: List[MessageReactionResponse] = Field(default_factory=dict, description="Реакции сообщения")
	# media_file_ids: List[UUID] = Field(default_factory=list, description="ID медиафайлов")

