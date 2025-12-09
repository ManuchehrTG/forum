from typing import List

from app.domains.user.schemas import User
from app.domains.theme.schemas import Theme
from app.domains.section.schemas import Section
from ..repositories import MessageCommentRepository
from ..schemas import MessageCommentCreateRequest, MessageWithComment
from .message import MessageService

class MessageCommentService:
	def __init__(self, message_service: MessageService):
		self.ALLOWED_SECTIONS = [
			"chat_ideas",
			"chat_qa",
			"chat_publications",
			# "chat_tasks",
			# "chat_experiments",
			"experience_exchange",
			"description",
			"perfect_result",
			"discussion",
		]
		self.SECTIONS_WITHOUT_CONTENT_ID = ["discussion"]
		self.SECTIONS_WITH_CONTENT_ID = [
			section_code for section_code in self.ALLOWED_SECTIONS
			if section_code not in self.SECTIONS_WITHOUT_CONTENT_ID
		]
		self.message_service = message_service

	async def create_message_comment(self, data: MessageCommentCreateRequest, user: User, theme: Theme, section: Section) -> MessageWithComment:
		# TODO: USE Transaction

		self.message_service._validate_section_access(section=section, allowed_sections=self.ALLOWED_SECTIONS)
		self.message_service._validate_message_field_requirement(
			section=section,
			required_sections=self.SECTIONS_WITH_CONTENT_ID,
			field_name="content_id",
			field_value=data.content_id
		)

		await self.message_service._validate_message_exists(section=section, message_type="post", message_name="Content", message_id=data.content_id)
		await self.message_service._validate_message_exists(section=section, message_type="comment", message_name="Reply message", message_id=data.reply_to_message_id)

		if section.code not in self.SECTIONS_WITH_CONTENT_ID:
			data.content_id = None

		message = await self.message_service._create_message(data=data, user=user, theme=theme, section=section)
		message_comment = await MessageCommentRepository.create_message_comment(data=data, message_id=message.id)

		return MessageWithComment(message=message, message_comment=message_comment)

	async def get_message_comments(self, user: User, theme: Theme, section: Section, content_id: int, limit: int, offset: int) -> List[MessageWithComment]:
		return await MessageCommentRepository.get_message_with_comments(
			theme_id=theme.id,
			section_code=section.code,
			content_id=content_id,
			limit=limit,
			offset=offset
		)
