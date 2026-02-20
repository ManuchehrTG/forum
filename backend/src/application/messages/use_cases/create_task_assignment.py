from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.messages.commands import CreateTaskAssignmentCommand
from src.application.messages.services.media_attachment import MessageMediaAttachmentService
from src.domain.media_files.repository import MediaFileRepository
from src.domain.messages.entities import Message
from src.domain.messages.exceptions import MessageNotFoundError
from src.domain.messages.repository import MessageRepository
from src.domain.messages.value_objects import MessageType
from src.domain.sections.repository import SectionRepository

class CreateTaskAssignment:
	def __init__(
		self,
		message_repo: MessageRepository,
		section_repo: SectionRepository,
		media_file_repo: MediaFileRepository,
		media_attachment_service: MessageMediaAttachmentService
	):
		self.message_repo = message_repo
		self.section_repo = section_repo
		self.media_file_repo = media_file_repo
		self.media_attachment_service = media_attachment_service

	@handle_domain_errors
	async def execute(self, command: CreateTaskAssignmentCommand) -> UUID:
		section = await self.section_repo.get_by_id(command.section_id)

		section.ensure_allowed_message_type(MessageType.TASK_ASSIGNMENT)

		try:
			content = await self.message_repo.get_by_id(command.content_id)
		except MessageNotFoundError:
			raise MessageNotFoundError.by_id_and_type(command.content_id, MessageType.TASK)

		content.ensure_is_task()

		message = Message.create_task_assignment(
			author_id=command.author_id,
			theme_id=command.theme_id,
			section_id=command.section_id,
			text=command.text,
			is_openai_generated=command.is_openai_generated,
			content_id=command.content_id,
			expires_at=command.expires_at,
			is_partially=command.is_partially
		)

		media_files = await self.media_file_repo.get_many_by_ids(command.media_file_ids)

		await self.media_attachment_service.attach_to_message(author_id=command.author_id, message=message, media_files=media_files)
		message.ensure_required_fields()

		await self.media_file_repo.save_many(media_files)
		await self.message_repo.save(message)

		return message.id
