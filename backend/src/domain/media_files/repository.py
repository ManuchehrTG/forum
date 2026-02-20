from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.media_files.entities import MediaFile

class MediaFileRepository(ABC):
	"""Интерфейс репозитория медиа-файлов"""
	# @abstractmethod
	# async def get_by_id(self, media_file_id: UUID) -> MediaFile:
	# 	pass

	@abstractmethod
	async def save(self, media_file: MediaFile) -> None:
		pass

	@abstractmethod
	async def save_many(self, media_files: List[MediaFile]) -> None:
		pass

	@abstractmethod
	async def get_many_by_ids(self, media_file_ids: List[UUID]) -> List[MediaFile]:
		pass
