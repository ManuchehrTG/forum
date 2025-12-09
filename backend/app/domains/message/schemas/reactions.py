from datetime import datetime
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from uuid import UUID

class MessageReactionType(str, Enum):
	LIKE = "like"
	DISLIKE = "dislike"

class MessageReaction(BaseModel):
	id: int = Field(..., description="ID реакции")
	message_id: int = Field(..., description="ID сообщения")
	user_id: UUID = Field(..., description="ID пользователя")
	reaction: MessageReactionType = Field(..., description="Реакция")
	created_at: datetime = Field(..., description="Дата создания")
	updated_at: datetime = Field(..., description="Дата обновления")

class MessageReactionUpdateRequest(BaseModel):
	reaction: MessageReactionType = Field(..., description="Реакция")

class MessageReactionResponse(BaseModel):
	# message_id: int = Field(..., description="ID сообщения")
	user_id: UUID = Field(..., description="ID пользователя")
	reaction: MessageReactionType = Field(..., description="Реакция")
	created_at: datetime = Field(..., description="Дата создания")
	updated_at: datetime = Field(..., description="Дата обновления")
