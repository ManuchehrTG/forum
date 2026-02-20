from pydantic import BaseModel
from uuid import UUID

class CreateThemeCommand(BaseModel):
	parent_id: UUID | None = None
	author_id: UUID
	title: str
	is_group: bool

	tech_version: str
