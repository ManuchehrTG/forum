from src.application.decorators import handle_domain_errors
from src.application.message_reactions.queries import GetMessageReactionStatsQuery
from src.application.message_reactions.dtos import MessageReactionStatsDTO
from src.domain.message_reactions.repository import MessageReactionRepository
from src.domain.message_reactions.value_objects import MessageReactionStats

class GetMessageReactionStats:
	def __init__(self, message_reaction_repo: MessageReactionRepository):
		self.message_reaction_repo = message_reaction_repo

	@handle_domain_errors
	async def execute(self, query: GetMessageReactionStatsQuery) -> MessageReactionStatsDTO:
		message_reaction_stats = await self.message_reaction_repo.get_stats(query.message_id)
		return self._to_dto(message_reaction_stats)

	def _to_dto(self, message_reaction_stats: MessageReactionStats) -> MessageReactionStatsDTO:
		return MessageReactionStatsDTO(
			reactions=message_reaction_stats.reactions,
			total=message_reaction_stats.total
		)
