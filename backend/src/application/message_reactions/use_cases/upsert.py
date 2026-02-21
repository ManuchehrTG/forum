from src.application.decorators import handle_domain_errors
from src.application.message_reactions.commands import UpsertMessageReactionCommand
from src.application.message_reactions.dtos import MessageReactionDTO
from src.domain.message_reactions.entities import MessageReaction
from src.domain.message_reactions.repository import MessageReactionRepository
from src.domain.message_reactions.value_objects import MessageReactionType

class UpsertMessageReaction:
	def __init__(self, message_reaction_repo: MessageReactionRepository):
		self.message_reaction_repo = message_reaction_repo

	@handle_domain_errors
	async def execute(self, command: UpsertMessageReactionCommand) -> MessageReactionDTO | None:
		reaction_enum = MessageReactionType(command.reaction) if command.reaction else None
		message_reaction = await self.message_reaction_repo.upsert(command.user_id, command.message_id, reaction_enum)
		if message_reaction:
			return self._to_dto(message_reaction)

	def _to_dto(self, message_reaction: MessageReaction) -> MessageReactionDTO:
		return MessageReactionDTO(
			user_id=message_reaction.user_id,
			message_id=message_reaction.message_id,
			updated_at=message_reaction.updated_at,
			reaction=message_reaction.reaction,
		)
