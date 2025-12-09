from fastapi import UploadFile
from typing import Any, List
from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domains.user.schemas import User
from app.domains.theme.schemas import Theme
from app.domains.theme.services import ThemeSectionService
from app.domains.section.exceptions import InvalidSectionError, MissingFieldForSectionError
from app.domains.section.schemas import Section
from app.domains.openai.exceptions import AIFeatureDisabledError
from app.domains.openai.schemas import OpenAIGenerateTextRequest, OpenAIGenerateText
from app.domains.openai.services import OpenAIService
from app.domains.media_file.schemas import MediaFile
from app.domains.media_file.services import MediaFileService
from ..repositories import MessageRepository
from ..schemas import (
	Message, MessageCreateRequest, MessageType,
	MessageReaction, MessageReactionUpdateRequest
)

class MessageService:
	def __init__(
		self,
		openai_service: OpenAIService,
		theme_section_service: ThemeSectionService,
		media_file_service: MediaFileService,
	):
		self.openai_service = openai_service
		self.theme_section_service = theme_section_service
		self.media_file_service = media_file_service

	async def generate_text(self, data: OpenAIGenerateTextRequest, user: User, theme: Theme, section: Section) -> OpenAIGenerateText:
		if not section.is_openai_enabled:
			raise AIFeatureDisabledError("OpenAI is disabled [1]")
		if not section.openai_prompt:
			raise AIFeatureDisabledError("OpenAI is disabled [2]")

		openai_text = await self.openai_service.generate_text(prompt=section.openai_prompt, text=data.text)
		return OpenAIGenerateText(original_text=data.text, openai_text=openai_text)

	async def _create_message(self, data: MessageCreateRequest, user: User, theme: Theme, section: Section) -> Message:
		message = await MessageRepository.create_message(data=data, author_id=user.id, theme_id=theme.id, section_code=section.code)
		media_file_ids = []

		if data.media_file_ids:
			media_files = await self.media_file_service.get_temporary_media_files_by_ids(media_file_ids=data.media_file_ids)
			if media_files:
				await self._attach_media_files(media_files=media_files, message_id=message.id)
				# media_file_ids = [media_file.id for media_file in media_files]

		return message

	async def get_message(self, message_id: int) -> Message:
		message = await MessageRepository.get_message_by_id(message_id=message_id)
		if not message:
			raise NotFoundError(entity="Message", entity_id=message_id)

		await self.theme_section_service._validate_theme_section_access(theme_id=message.theme_id, section_code=message.section_code)

		return message

	async def upload_files(self, files: List[UploadFile], user: User) -> List[UUID]:
		upload_subdir = "messages"
		media_files = await self.media_file_service.save_files(files=files, user=user, upload_subdir="messages", is_temp=True)
		return [media_file.id for media_file in media_files]

	async def get_message_media_files(self, message: Message) -> List[MediaFile]:
		media_file_ids = await MessageRepository.get_message_file_ids(message_id=message.id)
		return await self.media_file_service.get_media_files_by_ids(media_file_ids=media_file_ids)

	async def get_message_reactions(self, message_id: int) -> List[MessageReaction]:
		return await MessageRepository.get_message_reactions(message_id=message_id)

	async def message_update_reaction(self, data: MessageReactionUpdateRequest, user: User, message: Message) -> List[MessageReaction]:
		await MessageRepository.update_message_reaction(user_id=user.id, message_id=message.id, reaction=data.reaction)
		return await self.get_message_reactions(message_id=message.id)

	async def _attach_media_files(self, media_files: List[MediaFile], message_id: int) -> None:
		await self.media_file_service.activate_media_files(media_files=media_files)
		await MessageRepository.create_message_files(media_files=media_files, message_id=message_id)


	def _validate_section_access(self, section: Section, allowed_sections: List[str]) -> None:
		"""Валидация доступа к секции"""
		if section.code not in allowed_sections:
			raise InvalidSectionError(section_code=section.code, allowed_sections=allowed_sections)

	def _validate_message_field_requirement(
		self,
		section: Section,
		required_sections: List[str],
		field_name: str,
		field_value: Any
	) -> None:
		"""Валидация требования field_name & field_value для секции"""
		if section.code in required_sections and field_value is None:
			raise MissingFieldForSectionError(
				field=field_name,
				section_code=section.code,
				sections_requiring_field=required_sections
			)

	async def _validate_message_exists(self, section: Section, message_type: MessageType, message_name: str, message_id: int) -> None:
		"""Валидация существования Message"""
		if not message_id:
			return

		try:
			message = await self.get_message(message_id=message_id)
		except NotFoundError:
			raise NotFoundError(
				entity=message_name,
				entity_id=message_id,
				details=f"The `{message_name}` you are trying to respond to has not been found"
			)

		# Упрощенная проверка
		if message.section_code != section.code or message.type != message_type:
			raise NotFoundError(
				entity=message_name,
				entity_id=message_id,
				details=f"The `{message_name}` you are trying to respond to has not been found"
			)
