from fastapi import Depends, HTTPException
from typing import List

from .factory import create_message_service, create_message_post_service, create_message_comment_service, create_message_task_service
from .schemas import Message, MessageReaction
from .services import MessageService, MessagePostService, MessageCommentService, MessageTaskService

def get_message_service() -> MessageService:
	return create_message_service()

def get_message_post_service() -> MessagePostService:
	return create_message_post_service()

def get_message_comment_service() -> MessageCommentService:
	return create_message_comment_service()

def get_message_task_service() -> MessageTaskService:
	return create_message_task_service()

async def get_message(
	message_id: int,
	message_service: MessageService = Depends(get_message_service)
) -> Message:
	return await message_service.get_message(message_id=message_id)

async def get_message_reactions(
	message: Message = Depends(get_message),
	message_service: MessageService = Depends(get_message_service)
) -> List[MessageReaction]:
	return await message_service.get_message_reactions(message_id=message.id)
