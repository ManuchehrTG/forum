from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.domain.messages.entities import Message
from src.domain.messages.value_objects import MessageType

class MessageRepository(ABC):
	"""Интерфейс репозитория сообщений"""
	@abstractmethod
	async def get_by_id(self, message_id: UUID) -> Message:
		pass

	@abstractmethod
	async def save(self, message: Message) -> None:
		pass

	@abstractmethod
	async def get_list(self, type: MessageType, theme_id: UUID, section_id: UUID, content_id: UUID | None = None, limit: int = 10, offset: int = 0) -> List[Message]:
		pass