from src.application.decorators import handle_domain_errors
from src.application.messages.dtos import MessageDTO
from src.application.messages.queries import GetMessageQuery
from src.domain.messages.entities import Message
from src.domain.messages.repository import MessageRepository
from src.domain.messages.value_objects import MessageType

class GetMessage:
	def __init__(self, message_repo: MessageRepository):
		self.message_repo = message_repo

	@handle_domain_errors
	async def execute(self, query: GetMessageQuery) -> MessageDTO:
		message = await self.message_repo.get_by_id(query.message_id)

		return self._to_dto(message)

	def _to_dto(self, message: Message) -> MessageDTO:
		dto = MessageDTO(
			id=message.id,
			author_id=message.author_id,
			theme_id=message.theme_id,
			section_id=message.section_id,
			type=message.type,
			text=message.text,
			is_openai_generated=message.is_openai_generated,
			created_at=message.created_at,
			updated_at=message.updated_at,
		)

		if message.type == MessageType.POST:
			pass

		elif message.type == MessageType.TASK:
			dto.ratio = message.task_data.ratio										# pyright: ignore[reportOptionalMemberAccess]

		elif message.type == MessageType.TASK_ASSIGNMENT:
			dto.content_id = message.task_assignment_data.content_id				# pyright: ignore[reportOptionalMemberAccess]
			dto.is_partially = message.task_assignment_data.is_partially			# pyright: ignore[reportOptionalMemberAccess]
			dto.status = message.task_assignment_data.status						# pyright: ignore[reportOptionalMemberAccess]
			dto.expires_at = message.task_assignment_data.expires_at				# pyright: ignore[reportOptionalMemberAccess]

		elif message.type == MessageType.COMMENT:
			dto.content_id = message.comment_data.content_id						# pyright: ignore[reportOptionalMemberAccess]
			dto.reply_to_message_id = message.comment_data.reply_to_message_id		# pyright: ignore[reportOptionalMemberAccess]

		return dto

