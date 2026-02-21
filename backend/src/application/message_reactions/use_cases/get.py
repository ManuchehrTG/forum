from src.application.decorators import handle_domain_errors
from src.application.message_reactions.queries import GetMessageReactionQuery
from src.application.message_reactions.dtos import MessageReactionDTO
from src.domain.message_reactions.entities import MessageReaction
from src.domain.message_reactions.repository import MessageReactionRepository

class GetMessageReaction:
	def __init__(self, message_reaction_repo: MessageReactionRepository):
		self.message_reaction_repo = message_reaction_repo

	@handle_domain_errors
	async def execute(self, query: GetMessageReactionQuery) -> MessageReactionDTO:
		message_reaction = await self.message_reaction_repo.get_user_reaction(query.user_id, query.message_id)
		return self._to_dto(message_reaction)

	def _to_dto(self, message_reaction: MessageReaction) -> MessageReactionDTO:
		return MessageReactionDTO(
			user_id=message_reaction.user_id,
			message_id=message_reaction.message_id,
			updated_at=message_reaction.updated_at,
			reaction=message_reaction.reaction,
		)
