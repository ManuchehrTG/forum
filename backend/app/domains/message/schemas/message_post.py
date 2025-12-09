import json
from pydantic import BaseModel, Field
from typing import Literal

from .base import Message, MessageBase, MessageType, MessageResponse

class MessagePost(BaseModel):
	message_id: int = Field(..., description="ID сообщения")
	is_openai_generated: bool = Field(..., description="Сгенерировано с помощью openai или нет")
	ratio: int | None = Field(None, description="Коэффициент для задачи", ge=0, le=99)

class MessagePostCreateRequest(MessageBase):
	type: Literal[MessageType.POST] = MessageType.POST
	text: str = Field(..., description="Для обычного сообщения текст обязателен")
	is_openai_generated: bool = Field(False, description="Сгенерировано с помощью openai или нет")
	ratio: int | None = Field(None, description="Коэффициент для задачи. Только для chat_task & chat_experiments", ge=1, le=99)

class MessagePostResponse(BaseModel):
	is_openai_generated: bool = Field(..., description="Сгенерировано с помощью openai или нет")
	ratio: int | None = Field(None, description="Коэффициент для задачи", ge=0, le=99)

class MessageWithPost(BaseModel):
	message: Message
	message_post: MessagePost

	@classmethod
	def from_db_record(cls, record):
		"""Создает из записи БД с JSON строками"""
		message_data = record["message_json"]
		message_post_data = record["message_post_json"]

		if isinstance(message_data, str):
			message_data = json.loads(message_data)
		if isinstance(message_post_data, str):
			message_post_data = json.loads(message_post_data)

		return cls(
			message=Message(**message_data),
			message_post=MessagePost(**message_post_data)
		)

class MessageWithPostResponse(BaseModel):
	message: MessageResponse
	message_post: MessagePostResponse
