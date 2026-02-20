from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class ThemeDTO(BaseModel):
	id: UUID
	parent_id: UUID | None
	author_id: UUID | None
	title: str
	is_group: bool

	created_at: datetime
	updated_at: datetime

class ThemeSectionDTO(BaseModel):
	section_id: UUID
	section_code: str
