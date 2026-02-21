from uuid import UUID
from pydantic import BaseModel

class UpsertMessageReactionCommand(BaseModel):
	user_id: UUID
	message_id: UUID
	reaction: str | None
