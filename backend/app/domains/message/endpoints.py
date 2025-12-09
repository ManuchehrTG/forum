from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from typing import List
from uuid import UUID

from app.domains.auth.dependencies import get_current_user
from app.domains.user.schemas import User
from app.domains.theme.dependencies import get_theme, get_theme_section
from app.domains.theme.schemas import Theme
from app.domains.section.schemas import Section
from app.domains.openai.exceptions import AIFeatureDisabledError
from app.domains.openai.schemas import OpenAIGenerateTextRequest, OpenAIGenerateTextResponse
from app.domains.media_file.schemas import MediaFile, MediaFileResponse
from .adapters import (
	openai_generate_text_to_response,
	message_to_response, message_post_to_response, message_task_to_response, message_comment_to_response,
	message_with_post_to_response, message_with_task_to_response, message_with_comment_to_response,
	media_file_to_response,
	message_reaction_to_response
)
from .dependencies import get_message_service, get_message_post_service, get_message_comment_service, get_message_task_service, get_message, get_message_reactions
from .schemas import (
	Message, MessageResponse,
	MessagePostCreateRequest, MessageWithPostResponse,
	MessageCommentCreateRequest, MessageWithCommentResponse,
	MessageTaskCreateRequest, MessageWithTaskResponse,
	MessageReaction, MessageReactionUpdateRequest, MessageReactionResponse
)
from .services import MessageService, MessagePostService, MessageCommentService, MessageTaskService

router = APIRouter(prefix="/api/v1/messages", tags=["Messages"])

@router.post("/openai", response_model=OpenAIGenerateTextResponse)
async def message_openai_generate_text_endpoint(
	data: OpenAIGenerateTextRequest,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_service: MessageService = Depends(get_message_service)
):
	openai_generate_text = await message_service.generate_text(data=data, user=user, theme=theme, section=section)
	return openai_generate_text_to_response(openai_generate_text=openai_generate_text)

@router.post("/posts", response_model=MessageWithPostResponse)
async def create_message_post_endpoint(
	data: MessagePostCreateRequest,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_post_service: MessagePostService = Depends(get_message_post_service)
):
	message_with_post = await message_post_service.create_message_post(data=data, user=user, theme=theme, section=section)
	return message_with_post_to_response(message_with_post=message_with_post)

@router.get("/posts", response_model=List[MessageWithPostResponse])
async def get_message_posts_endpoint(
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_post_service: MessagePostService = Depends(get_message_post_service),
	limit: int = Query(default=100, ge=1, le=500),
	offset: int = Query(default=0, ge=0)
):
	message_with_posts = await message_post_service.get_message_posts(user=user, theme=theme, section=section, limit=limit, offset=offset)
	return [
		message_with_post_to_response(message_with_post=message_with_post)
		for message_with_post in message_with_posts
	]

@router.post("/tasks", response_model=MessageWithTaskResponse)
async def create_message_task_endpoint(
	data: MessageTaskCreateRequest,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_task_service: MessageTaskService = Depends(get_message_task_service)
):
	message_with_task = await message_task_service.create_message_task(data=data, user=user, theme=theme, section=section)
	return message_with_task_to_response(message_with_task=message_with_task)

@router.get("/tasks/{content_id}", response_model=List[MessageWithTaskResponse])
async def get_message_tasks_endpoint(
	content_id: int,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_task_service: MessageTaskService = Depends(get_message_task_service),
	limit: int = Query(default=100, ge=1, le=500),
	offset: int = Query(default=0, ge=0)
):
	message_with_tasks = await message_task_service.get_message_tasks(user=user, theme=theme, section=section, content_id=content_id, limit=limit, offset=offset)
	return [
		message_with_task_to_response(message_with_task=message_with_task)
		for message_with_task in message_with_tasks
	]

@router.post("/comments", response_model=MessageWithCommentResponse)
async def create_message_comment_endpoint(
	data: MessageCommentCreateRequest,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_comment_service: MessageCommentService = Depends(get_message_comment_service)
):
	message_with_comment = await message_comment_service.create_message_comment(data=data, user=user, theme=theme, section=section)
	return message_with_comment_to_response(message_with_comment=message_with_comment)

@router.get("/comments/{content_id}", response_model=List[MessageWithCommentResponse])
async def get_message_comments_endpoint(
	content_id: int,
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_theme_section),
	message_comment_service: MessageCommentService = Depends(get_message_comment_service),
	limit: int = Query(default=100, ge=1, le=500),
	offset: int = Query(default=0, ge=0)
):
	message_with_comments = await message_comment_service.get_message_comments(user=user, theme=theme, section=section, content_id=content_id, limit=limit, offset=offset)
	return [
		message_with_comment_to_response(message_with_comment=message_with_comment)
		for message_with_comment in message_with_comments
	]

@router.post("/upload_files", response_model=List[UUID])
async def message_upload_files_endpoint(
	files: List[UploadFile],
	user: User = Depends(get_current_user),
	message_service: MessageService = Depends(get_message_service)
):
	return await message_service.upload_files(files=files, user=user)

@router.get("/{message_id}/attachments", response_model=List[MediaFileResponse])
async def get_message_media_files_endpoint(
	user: User = Depends(get_current_user),
	message: Message = Depends(get_message),
	message_service: MessageService = Depends(get_message_service)
):
	media_files = await message_service.get_message_media_files(message=message)
	return [
		media_file_to_response(media_file=media_file)
		for media_file in media_files
	]

@router.patch("/{message_id}/reaction", response_model=List[MessageReactionResponse])
async def create_message_reaction_endpoint(
	data: MessageReactionUpdateRequest,
	user: User = Depends(get_current_user),
	message: Message = Depends(get_message),
	message_service: MessageService = Depends(get_message_service)
):
	message_reactions = await message_service.message_update_reaction(data=data, user=user, message=message)
	return [
		message_reaction_to_response(message_reaction=message_reaction)
		for message_reaction in message_reactions
	]

@router.get("/{message_id}/reactions", response_model=List[MessageReactionResponse])
async def get_reactions_endpoint(
	user: User = Depends(get_current_user),
	message_reactions: List[MessageReaction] = Depends(get_message_reactions),
	message_service: MessageService = Depends(get_message_service)
):
	return [
		message_reaction_to_response(message_reaction=message_reaction)
		for message_reaction in message_reactions
	]
