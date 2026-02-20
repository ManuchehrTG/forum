from pydantic import BaseModel
from uuid import UUID

class SectionResponse(BaseModel):
	id: UUID
	code: str
