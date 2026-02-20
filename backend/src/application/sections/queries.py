from enum import Enum
from pydantic import BaseModel
from uuid import UUID

class GetSectionQueryType(str, Enum):
	BY_ID = "by_id"
	BY_CODE = "by_code"

class GetSectionQuery(BaseModel):
	"""Базовый query для получения секций"""
	query_type: GetSectionQueryType
	params: dict

	@classmethod
	def by_id(cls, section_id: UUID) -> "GetSectionQuery":
		return cls(
			query_type=GetSectionQueryType.BY_ID,
			params={"section_id": section_id}
		)

	@classmethod
	def by_code(cls, section_code: str) -> "GetSectionQuery":
		return cls(
			query_type=GetSectionQueryType.BY_CODE,
			params={"section_code": section_code}
		)
