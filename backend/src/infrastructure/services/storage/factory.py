from pathlib import Path

from .local_storage import LocalStorageService
from src.core.config import settings
# from src.infrastructure.services.storage.s3_storage import S3StorageService

def create_storage_service():
	"""Фабрика для создания storage service в зависимости от окружения"""
	# if settings.STORAGE_TYPE == "s3":
	#     return S3StorageService(
	#         bucket=settings.S3_BUCKET,
	#         access_key=settings.S3_ACCESS_KEY,
	#         secret_key=settings.S3_SECRET_KEY,
	#         cdn_url=settings.CDN_URL
	#     )
	# else:
	return LocalStorageService(base_path=Path(settings.storage.dir), base_url=f"/{settings.storage.dir}")
