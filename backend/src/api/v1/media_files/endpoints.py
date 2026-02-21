from fastapi import APIRouter, Depends, UploadFile
from typing import List
from uuid import UUID

from .dependencies import get_upload_files
from src.api.v1.users.dependencies import get_current_user
from src.application.media_files.commands import UploadFilesCommand
from src.application.media_files.use_cases.upload_files import UploadFiles
from src.application.users.dtos import UserDTO

router = APIRouter(prefix="/media_files", tags=["MediaFiles"])

@router.post("/uploads", response_model=List[UUID], summary="Upload media files", description="<b>Загрузка медифайлов в временное хранилище.</b>")
async def uploads_endpoint(
	files: List[UploadFile],
	user: UserDTO = Depends(get_current_user),
	upload_files: UploadFiles = Depends(get_upload_files)
):
	command = UploadFilesCommand(author_id=user.id, files=files)
	media_file_ids = await upload_files.execute(command)
	return media_file_ids
