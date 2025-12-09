import json
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
from typing import Literal

from .base import Message, MessageBase, MessageType, MessageResponse

class MessageTaskStatusType(str, Enum):
	IN_PROGRESS = "in_progress"
	SUCCESSFUL = "successful"
	FAILED = "failed"

class MessageTask(BaseModel):
	message_id: int = Field(..., description="ID сообщения")
	content_id: int = Field(..., description="ID контента (сообщения) к которому относится `задача в работе`")
	is_partially: bool = Field(..., description="Выполняемая задача частичная или нет (полная)")
	status: MessageTaskStatusType = Field(..., description="Статус выполняемой задачи")
	expires_at: datetime = Field(..., description="Дата истечения")

class MessageTaskCreateRequest(MessageBase):
	type: Literal[MessageType.TASK] = MessageType.TASK
	content_id: int = Field(..., description="ID контента (сообщения) к которому относится `задача в работе`")
	text: str = Field(..., description="Для задачи текст обязателен")
	is_partially: bool = Field(False, description="Выполняемая задача частичная или нет (полная)")
	expires_at: datetime = Field(..., description="Дата истечения")

class MessageTaskResponse(BaseModel):
	content_id: int = Field(..., description="ID контента (сообщения) к которому относится `задача в работе`")
	is_partially: bool = Field(..., description="Выполняемая задача частичная или нет (полная)")
	status: MessageTaskStatusType = Field(..., description="Статус выполняемой задачи")
	expires_at: datetime = Field(..., description="Дата истечения")

class MessageWithTask(BaseModel):
	message: Message
	message_task: MessageTask

	@classmethod
	def from_db_record(cls, record):
		"""Создает из записи БД с JSON строками"""
		message_data = record["message_json"]
		message_task_data = record["message_task_json"]

		if isinstance(message_data, str):
			message_data = json.loads(message_data)
		if isinstance(message_task_data, str):
			message_task_data = json.loads(message_task_data)

		return cls(
			message=Message(**message_data),
			message_task=MessageTask(**message_task_data)
		)

class MessageWithTaskResponse(BaseModel):
	message: MessageResponse
	message_task: MessageTaskResponse
