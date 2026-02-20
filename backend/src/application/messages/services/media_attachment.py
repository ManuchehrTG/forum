from typing import List
from uuid import UUID

from src.domain.interfaces.storage_service import StorageService
from src.domain.media_files.entities import MediaFile
from src.domain.messages.entities.message import Message

class MessageMediaAttachmentService:
	"""
	Доменный сервис для работы с медиафайлами сообщений
	Содержит бизнес-логику прикрепления файлов к сообщению
	"""

	def __init__(self, storage_service: StorageService):
		self.storage_service = storage_service

	async def attach_to_message(self, author_id: UUID, message: Message, media_files: List[MediaFile]) -> None:
		"""
		Прикрепить медиафайлы к сообщению
		Содержит всю бизнес-логику работы с файлами
		"""
		for mf in media_files:
			mf.ensure_author(author_id)
			mf.ensure_is_temp()
			message.add_media_file(mf.id)

			new_path = f"messages/{message.id}/{mf.filename}"

			self.storage_service.move(source_path=mf.storage_path, new_path=new_path)
			mf.promote(new_path)
