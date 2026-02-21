from datetime import datetime
from uuid import UUID

from src.domain.message_reactions.value_objects import MessageReactionType

class MessageReaction:
	def __init__(
		self,
		id: UUID,
		user_id: UUID,
		message_id: UUID,
		reaction: MessageReactionType,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
	) -> None:
		self.id = id
		self.user_id = user_id
		self.message_id = message_id
		self.reaction = reaction
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or self.created_at

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			user_id=record["user_id"],
			message_id=record["message_id"],
			reaction=MessageReactionType(record["reaction"]),
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)
