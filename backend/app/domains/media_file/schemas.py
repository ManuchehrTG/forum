import json
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from uuid import UUID

class MediaFileStatusType(str, Enum):
	TEMPORARY = "temporary"
	ATTACHED = "attached"

class MediaFile(BaseModel):
	id: UUID
	author_id: UUID
	file_path: str
	original_name: str
	mime_type: str
	file_size: int
	status: MediaFileStatusType
	metadata: dict = Field(default_factory=dict)
	expires_at: datetime | None
	created_at: datetime
	updated_at: datetime

	@field_validator('metadata', mode='before')
	@classmethod
	def validate_metadata(cls, v):
		if isinstance(v, str):
			try:
				return json.loads(v)
			except json.JSONDecodeError:
				return {}
		return v

class MediaFileCreateData(BaseModel):
	author_id: UUID
	file_path: str
	original_name: str
	mime_type: str
	file_size: int
	status: MediaFileStatusType
	metadata: dict = Field(default_factory=dict)
	expires_at: datetime | None = None

class MediaFileResponse(BaseModel):
	file_path: str
	original_name: str
	mime_type: str
	file_size: int
	created_at: datetime
