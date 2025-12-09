import json
from pydantic import BaseModel, Field
from typing import Literal

from .base import Message, MessageBase, MessageType, MessageResponse

class MessageComment(BaseModel):
	message_id: int = Field(..., description="ID сообщения")
	content_id: int | None = Field(None, description="ID контента (сообщения) к которому относится комментарий")
	reply_to_message_id: str | None = Field(None, description="ID комментария (сообщения) к которому предназначен ответ")

class MessageCommentCreateRequest(MessageBase):
	type: Literal[MessageType.COMMENT] = MessageType.COMMENT
	content_id: int | None = Field(None, description="ID контента (сообщения) к которому относится комментарий", ge=1)
	reply_to_message_id: int | None = Field(None, description="ID комментария (сообщения) к которому предназначен ответ", ge=1)

class MessageCommentResponse(BaseModel):
	content_id: int | None = Field(None, description="ID контента (сообщения) к которому относится комментарий")
	reply_to_message_id: int | None = Field(None, description="ID комментария (сообщения) к которому предназначен ответ")

class MessageWithComment(BaseModel):
	message: Message
	message_comment: MessageComment

	@classmethod
	def from_db_record(cls, record):
		"""Создает из записи БД с JSON строками"""
		message_data = record["message_json"]
		message_comment_data = record["message_comment_json"]

		if isinstance(message_data, str):
			message_data = json.loads(message_data)
		if isinstance(message_comment_data, str):
			message_comment_data = json.loads(message_comment_data)

		return cls(
			message=Message(**message_data),
			message_comment=MessageComment(**message_comment_data)
		)

class MessageWithCommentResponse(BaseModel):
	message: MessageResponse
	message_comment: MessageCommentResponse
