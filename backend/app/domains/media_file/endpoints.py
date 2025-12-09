# from fastapi import APIRouter, Depends, File, UploadFile
# from typing import List

# from app.domains.auth.dependencies import get_current_user
# from app.domains.user.schemas import User
# from .schemas import MediaFileResponse
# from .services import MediaFileService

# router = APIRouter(prefix="/api/v1/media", tags=["Media"])

# @router.post("/uploads", response_model=List[MediaFileResponse])
# async def upload_media_files_endpoint(
# 	files: List[UploadFile],
# 	user: User = Depends(get_current_user),
# 	media_file_service: MediaFileService = Depends(get_media_file_service)
# ):
# 	return await media_file_service.save_files(files=files, user=user)

# @router.post("/upload", response_model=MediaFileResponse)
# async def upload_media_file_endpoint(
# 	file: UploadFile = File(...),
# 	user: User = Depends(get_current_user),
# 	media_file_service: MediaFileService = Depends(get_media_file_service)
# ):
# 	return await media_file_service.upload_file(file=file, user=user)

# # @router.get("/{media_file_url:path}")
# # async def download_media_file_endpoint(
# # 	media_file_url: str
# # ):
# # 	return await MediaFileService.download_file(url=media_file_url, subdir="media_files")
