from app.domains.openai.services import OpenAIService
from app.domains.theme.services import ThemeSectionService
from app.domains.media_file.services import MediaFileService
from .services import MessageService, MessagePostService, MessageTaskService, MessageCommentService

def create_message_service() -> MessageService:
	return MessageService(
		openai_service=OpenAIService(),
		theme_section_service=ThemeSectionService(),
		media_file_service=MediaFileService()
	)

def create_message_post_service() -> MessagePostService:
	return MessagePostService(
		message_service=create_message_service()
	)

def create_message_comment_service() -> MessageCommentService:
	return MessageCommentService(
		message_service=create_message_service()
	)

def create_message_task_service() -> MessageTaskService:
	return MessageTaskService(
		message_service=create_message_service()
	)
