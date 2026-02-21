from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.message_reactions.entities import MessageReaction
from src.domain.message_reactions.value_objects import MessageReactionType, MessageReactionStats

class MessageReactionRepository(ABC):
	"""Интерфейс репозитория реакций сообщения"""
	@abstractmethod
	async def get_user_reaction(self, user_id: UUID, message_id: UUID) -> MessageReaction:
		pass

	@abstractmethod
	async def upsert(self, user_id: UUID, message_id: UUID, reaction: MessageReactionType | None) -> MessageReaction | None:
		pass

	@abstractmethod
	async def get_stats(self, message_id: UUID) -> MessageReactionStats:
		pass
