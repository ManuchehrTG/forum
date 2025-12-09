from typing import List

from app.domains.user.schemas import User
from app.domains.theme.schemas import Theme
from app.domains.section.schemas import Section
from ..repositories import MessagePostRepository
from ..schemas import MessagePostCreateRequest, MessageWithPost
from .message import MessageService

class MessagePostService:
	def __init__(self, message_service: MessageService):
		self.ALLOWED_SECTIONS = [
			"chat_ideas",
			"chat_qa",
			"chat_publications",
			"chat_tasks",
			"chat_experiments",
			# "project_modules",
			# "discussion",
			"experience_exchange",
			"description",
			"perfect_result",
		]
		self.SECTIONS_WITH_RATIO = ["chat_tasks", "chat_experiments"]
		self.SECTIONS_WITHOUT_RATIO = [
			section_code for section_code in self.ALLOWED_SECTIONS
			if section_code not in self.SECTIONS_WITH_RATIO
		]
		self.message_service = message_service

	async def create_message_post(self, data: MessagePostCreateRequest, user: User, theme: Theme, section: Section) -> MessageWithPost:
		# TODO: USE Transaction

		self.message_service._validate_section_access(section=section, allowed_sections=self.ALLOWED_SECTIONS)
		self.message_service._validate_message_field_requirement(
			section=section,
			required_sections=self.SECTIONS_WITH_RATIO,
			field_name="ratio",
			field_value=data.ratio
		)

		if section.code not in self.SECTIONS_WITH_RATIO:
			data.ratio = None

		message = await self.message_service._create_message(data=data, user=user, theme=theme, section=section)
		message_post = await MessagePostRepository.create_message_post(data=data, message_id=message.id)

		return MessageWithPost(message=message, message_post=message_post)

	async def get_message_posts(self, user: User, theme: Theme, section: Section, limit: int, offset: int) -> List[MessageWithPost]:
		return await MessagePostRepository.get_message_with_posts(
			theme_id=theme.id,
			section_code=section.code,
			limit=limit,
			offset=offset
		)
