from datetime import datetime
from pydantic import BaseModel
from typing import Dict
from uuid import UUID

from src.domain.message_reactions.value_objects import MessageReactionType

class MessageReactionDTO(BaseModel):
	user_id: UUID
	message_id: UUID
	reaction: MessageReactionType | None
	updated_at: datetime

class MessageReactionStatsDTO(BaseModel):
	reactions: Dict[MessageReactionType, int]
	total: int
