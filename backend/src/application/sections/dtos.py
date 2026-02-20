from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

from src.domain.sections.value_objects import TechVersionType

class SectionDTO(BaseModel):
	id: UUID
	code: str
	openai_prompt: str | None
	tech_version: TechVersionType
	enable_openai: bool
	allow_hide: bool

	created_at: datetime
	updated_at: datetime
