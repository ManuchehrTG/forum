from pydantic import BaseModel
from typing import List
from uuid import UUID

class GetFilesQuery(BaseModel):
	"""Query для получения файлов"""
	media_file_ids: List[UUID]
