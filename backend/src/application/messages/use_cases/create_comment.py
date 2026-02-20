from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.messages.commands import CreateCommentCommand
from src.application.messages.services.media_attachment import MessageMediaAttachmentService
from src.domain.media_files.repository import MediaFileRepository
from src.domain.messages.entities import Message
from src.domain.messages.repository import MessageRepository
from src.domain.sections.repository import SectionRepository

class CreateComment:
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
	async def execute(self, command: CreateCommentCommand) -> UUID:
		section = await self.section_repo.get_by_id(command.section_id)

		content = await self.message_repo.get_by_id(command.content_id)
		# Проверка может ли контент принимать комментарии пока-что не нужна, т.к. данное разрешение всегда True, а вот в каой секции можно или нет решает Section

		section.ensure_allowed_comment_for_message_type(content.type) # Секция не знает про MessageType

		if command.reply_to_message_id:
			reply_to_message = await self.message_repo.get_by_id(command.reply_to_message_id)
			reply_to_message.ensure_is_comment()
			reply_to_message.ensure_content(content.id)

		message = Message.create_comment(
			author_id=command.author_id,
			theme_id=command.theme_id,
			section_id=command.section_id,
			text=command.text,
			is_openai_generated=command.is_openai_generated,
			content_id=command.content_id,
			reply_to_message_id=command.reply_to_message_id
		)

		media_files = await self.media_file_repo.get_many_by_ids(command.media_file_ids)

		await self.media_attachment_service.attach_to_message(author_id=command.author_id, message=message, media_files=media_files)
		message.ensure_required_fields()

		await self.media_file_repo.save_many(media_files)
		await self.message_repo.save(message)

		return message.id
