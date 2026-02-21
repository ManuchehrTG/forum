from uuid import UUID

from src.shared.exceptions import NotFoundError

class MessageReactionNotFoundError(NotFoundError):
	"""Реакция на сообщение не найдена"""
	error_code = "message_reaction_not_found"

	def __init__(self, entity_id: str | UUID, search_type: str, **kwargs):
		super().__init__(entity="MessageReaction", entity_id=str(entity_id), search_type=search_type, **kwargs)

	@classmethod
	def by_user_and_message(cls, user_id: UUID, message_id: UUID, **kwargs) -> "MessageReactionNotFoundError":
		"""Реакция пользователя на сообщение не найдена"""
		return cls(
			entity_id=f"user:{user_id}_message:{message_id}",
			search_type=f"user_id and message_id",
			message_id=str(message_id),
			user_id=str(user_id),
			**kwargs
		)
