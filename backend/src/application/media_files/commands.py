from fastapi import UploadFile
from pydantic import BaseModel
from typing import List
from uuid import UUID

class UploadFilesCommand(BaseModel):
	"""Команда для загрузки медиафайлов"""
	author_id: UUID
	files: List[UploadFile]
	is_temp: bool = True
