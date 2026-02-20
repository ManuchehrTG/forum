from src.application.decorators import handle_domain_errors
from src.application.messages.dtos import MessageDTO, MessageMediaFileDTO
from src.application.messages.queries import GetPostQuery
from src.domain.messages.entities import Message
from src.domain.messages.repository import MessageRepository

class GetPost:
	def __init__(self, message_repo: MessageRepository):
		self.message_repo = message_repo

	@handle_domain_errors
	async def execute(self, query: GetPostQuery) -> MessageDTO:
		message = await self.message_repo.get_by_id(query.post_id)

		message.ensure_is_post()

		return self._to_dto(message)

	def _to_dto(self, message: Message) -> MessageDTO:
		return MessageDTO(
			id=message.id,
			author_id=message.author_id,
			theme_id=message.theme_id,
			section_id=message.section_id,
			type=message.type,
			text=message.text,
			is_openai_generated=message.is_openai_generated,
			created_at=message.created_at,
			updated_at=message.updated_at,
			media_files=[MessageMediaFileDTO(media_file_id=mf.media_file_id, sort_order=mf.sort_order) for mf in message._media_files]
		)

