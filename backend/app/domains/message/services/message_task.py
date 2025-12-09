from typing import List

from app.domains.user.schemas import User
from app.domains.theme.schemas import Theme
from app.domains.section.schemas import Section
from ..repositories import MessageTaskRepository
from ..schemas import MessageTaskCreateRequest, MessageWithTask
from .message import MessageService

class MessageTaskService:
	def __init__(self, message_service: MessageService):
		self.ALLOWED_SECTIONS = ["chat_tasks", "chat_experiments"]
		self.message_service = message_service

	async def create_message_task(self, data: MessageTaskCreateRequest, user: User, theme: Theme, section: Section) -> MessageWithTask:
		# TODO: USE Transaction

		self.message_service._validate_section_access(section=section, allowed_sections=self.ALLOWED_SECTIONS)
		await self.message_service._validate_message_exists(section=section, message_type="post", message_name="Content", message_id=data.content_id)

		message = await self.message_service._create_message(data=data, user=user, theme=theme, section=section)
		message_task = await MessageTaskRepository.create_message_task(data=data, message_id=message.id)

		return MessageWithTask(message=message, message_task=message_task)

	async def get_message_tasks(self, user: User, theme: Theme, section: Section, content_id: int, limit: int, offset: int) -> List[MessageWithTask]:
		return await MessageTaskRepository.get_message_with_tasks(
			theme_id=theme.id,
			section_code=section.code,
			content_id=content_id,
			limit=limit,
			offset=offset
		)
