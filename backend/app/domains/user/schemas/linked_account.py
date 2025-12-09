import json
from pydantic import BaseModel, Field, field_validator
from uuid import UUID

from app.utils.serializers import dict_to_ns

class LinkedAccountCreateData(BaseModel):
	user_id: UUID
	provider: str
	provider_user_id: str | None = None
	extra: dict = {}

	@property
	def extra_obj(self):
		return self.dict_to_ns(self.extra)

	@property
	def extra_json(self):
		return json.dumps(self.extra)

	@field_validator("extra", mode="before")
	@classmethod
	def parse_extra(cls, value):
		if isinstance(value, str):
			return json.loads(value)
		return value

class LinkedAccount(LinkedAccountCreateData):
	id: UUID
