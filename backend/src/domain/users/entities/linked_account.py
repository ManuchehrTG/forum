import json
from datetime import datetime
from uuid import UUID, uuid4

from ..value_objects import AuthProviderType

class LinkedAccount:
	def __init__(
		self,
		user_id: UUID,
		provider: AuthProviderType,
		provider_user_id: str | None = None,
		extra: dict | None = None,
		id: UUID | None = None,
		created_at: datetime | None = None,
		updated_at: datetime | None = None
	) -> None:
		self.id = id or uuid4()
		self.user_id = user_id
		self.provider = provider
		self.provider_user_id = provider_user_id
		self.extra = extra or {}

		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			user_id=record["user_id"],
			provider=AuthProviderType(record["provider"]),
			provider_user_id=record["provider_user_id"],
			extra=json.loads(record["extra"]) if record["extra"] else {},
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)
