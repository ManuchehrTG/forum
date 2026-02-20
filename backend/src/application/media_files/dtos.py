from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class MediaFileDTO(BaseModel):
	id: UUID
	author_id: UUID
	filename: str
	original_filename: str
	file_size: int
	mime_type: str
	extension: str
	is_temp: bool
	created_at: datetime
	updated_at: datetime

	url: str
