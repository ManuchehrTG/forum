from enum import Enum
from pydantic import BaseModel
from uuid import UUID

class GetUserQueryType(str, Enum):
	BY_ID = "by_id"
	BY_PROVIDER_ID = "by_provider_id"

class GetUserQuery(BaseModel):
	"""Базовый query для получения пользователя"""
	query_type: GetUserQueryType
	params: dict

	@classmethod
	def by_id(cls, user_id: UUID) -> "GetUserQuery":
		return cls(
			query_type=GetUserQueryType.BY_ID,
			params={"user_id": user_id}
		)

	@classmethod
	def by_provider_id(cls, provider: str, provider_user_id: str) -> "GetUserQuery":
		return cls(
			query_type=GetUserQueryType.BY_PROVIDER_ID,
			params={"provider": provider, "provider_user_id": provider_user_id}
		)
