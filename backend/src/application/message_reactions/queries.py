from pydantic import BaseModel
from uuid import UUID

class GetMessageReactionQuery(BaseModel):
	user_id: UUID
	message_id: UUID

class GetMessageReactionStatsQuery(BaseModel):
	message_id: UUID
