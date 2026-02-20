from pydantic import BaseModel
from uuid import UUID

class GetThemeQuery(BaseModel):
	theme_id: UUID

class GetThemeSectionsQuery(BaseModel):
	theme_id: UUID
