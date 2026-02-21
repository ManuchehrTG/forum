from fastapi import APIRouter, Depends, Query, Response
from typing import List

from . import schemas
from .dependencies import (
	get_comment, get_create_comment, get_create_post, get_create_task_assignment, get_message, get_post, get_retrieve_comments, get_retrieve_posts,
	get_create_task, get_retrieve_task_assignments, get_task, get_retrieve_tasks, get_task_assignment,
	get_upsert_message_reaction, get_retrieve_message_reaction, get_retrieve_message_reaction_stats
)
from src.api.v1 import schemas as v1_schemas
from src.api.v1.sections.dependencies import get_section
from src.api.v1.themes.dependencies import get_theme
from src.api.v1.users.dependencies import get_current_user
from src.application.message_reactions.commands import UpsertMessageReactionCommand
from src.application.message_reactions.queries import GetMessageReactionQuery, GetMessageReactionStatsQuery
from src.application.message_reactions.use_cases.get import GetMessageReaction
from src.application.message_reactions.use_cases.get_stats import GetMessageReactionStats
from src.application.message_reactions.use_cases.upsert import UpsertMessageReaction
from src.application.messages.commands import CreateCommentCommand, CreatePostCommand, CreateTaskAssignmentCommand, CreateTaskCommand
from src.application.messages.dtos import MessageDTO
from src.application.messages.queries import GetCommentsQuery, GetPostsQuery, GetTaskAssignmentsQuery, GetTasksQuery
from src.application.messages.use_cases.create_comment import CreateComment
from src.application.messages.use_cases.create_post import CreatePost
from src.application.messages.use_cases.create_task import CreateTask
from src.application.messages.use_cases.create_task_assignment import CreateTaskAssignment
from src.application.messages.use_cases.get_comments import GetComments
from src.application.messages.use_cases.get_posts import GetPosts
from src.application.messages.use_cases.get_task_assignments import GetTaskAssignments
from src.application.messages.use_cases.get_tasks import GetTasks
from src.application.sections.dtos import SectionDTO
from src.application.themes.dtos import ThemeDTO
from src.application.users.dtos import UserDTO

router = APIRouter(prefix="/messages", tags=["Messages"])

# ЭНДПОИНТЫ ПОСТОВ
@router.post("/posts", response_model=v1_schemas.IdResponse, status_code=201)
async def create_post_endpoint(
	request: schemas.CreatePostRequest,
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	create_post: CreatePost = Depends(get_create_post),
):
	command = CreatePostCommand(author_id=user.id, theme_id=theme.id, section_id=section.id, **request.model_dump())
	message_id = await create_post.execute(command)
	return v1_schemas.IdResponse(id=message_id)

@router.get("/posts", response_model=List[schemas.PostMessageResponse])
async def get_posts_endpoint(
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	get_posts: GetPosts = Depends(get_retrieve_posts),
	limit: int = Query(default=100, ge=1, le=1000),
	offset: int = Query(default=0, ge=0)
):
	query = GetPostsQuery(theme_id=theme.id, section_id=section.id, limit=limit, offset=offset)
	posts = await get_posts.execute(query)
	return [schemas.PostMessageResponse.model_validate(post.model_dump()) for post in posts]

@router.get("/posts/{id}", response_model=schemas.PostMessageResponse)
async def get_post_endpoint(
	user: UserDTO = Depends(get_current_user),
	post: MessageDTO = Depends(get_post),
):
	return schemas.PostMessageResponse.model_validate(post.model_dump())


# ЭНДПОИНТЫ ЗАДАЧ
@router.post("/tasks", response_model=v1_schemas.IdResponse, status_code=201)
async def create_task_endpoint(
	request: schemas.CreateTaskRequest,
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	create_task: CreateTask = Depends(get_create_task)
):
	command = CreateTaskCommand(author_id=user.id, theme_id=theme.id, section_id=section.id, **request.model_dump())
	message_id = await create_task.execute(command)
	return v1_schemas.IdResponse(id=message_id)

@router.get("/tasks", response_model=List[schemas.TaskMessageResponse])
async def get_tasks_endpoint(
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	get_tasks: GetTasks = Depends(get_retrieve_tasks),
	limit: int = Query(default=100, ge=1, le=1000),
	offset: int = Query(default=0, ge=0)
):
	query = GetTasksQuery(theme_id=theme.id, section_id=section.id, limit=limit, offset=offset)
	tasks = await get_tasks.execute(query)
	return [schemas.TaskMessageResponse.model_validate(task.model_dump()) for task in tasks]

@router.get("/tasks/{id}", response_model=schemas.TaskMessageResponse)
async def get_task_endpoint(
	user: UserDTO = Depends(get_current_user),
	task: MessageDTO = Depends(get_task),
):
	return schemas.TaskMessageResponse.model_validate(task.model_dump())


# ЭНДПОИНТЫ НАЗНАЧАЕМЫХ ЗАДАЧ
@router.post("/tasks/{task_id}/assignment", response_model=v1_schemas.IdResponse, status_code=201)
async def create_task_assignment_endpoint(
	request: schemas.CreateTaskAssignmentRequest,
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	task: MessageDTO = Depends(get_task),
	create_task_assignment: CreateTaskAssignment = Depends(get_create_task_assignment)
):
	command = CreateTaskAssignmentCommand(author_id=user.id, theme_id=theme.id, section_id=section.id, content_id=task.id, **request.model_dump())
	message_id = await create_task_assignment.execute(command)
	return v1_schemas.IdResponse(id=message_id)

@router.get("/tasks/{task_id}/assignments", response_model=List[schemas.TaskAssignmentResponse])
async def get_task_assignments_endpoint(
	user: UserDTO = Depends(get_current_user),
	task: MessageDTO = Depends(get_task),
	get_task_assignments: GetTaskAssignments = Depends(get_retrieve_task_assignments),
	limit: int = Query(default=100, ge=1, le=1000),
	offset: int = Query(default=0, ge=0)
):
	query = GetTaskAssignmentsQuery(theme_id=task.theme_id, section_id=task.section_id, content_id=task.id, limit=limit, offset=offset)
	task_assignments = await get_task_assignments.execute(query)
	return [schemas.TaskAssignmentResponse.model_validate(task_assignment.model_dump()) for task_assignment in task_assignments]

@router.get("/tasks/assignments/{id}", response_model=schemas.TaskAssignmentResponse)
async def get_task_assignment_endpoint(
	user: UserDTO = Depends(get_current_user),
	task_assignment: MessageDTO = Depends(get_task_assignment),
):
	return schemas.TaskAssignmentResponse.model_validate(task_assignment.model_dump())


# ЭНДПОИНТЫ КОММЕНТАРИЕВ
@router.post("/{content_id}/comments", response_model=v1_schemas.IdResponse, status_code=201)
async def create_comment_endpoint(
	request: schemas.CreateCommentRequest,
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	section: SectionDTO = Depends(get_section),
	content: MessageDTO = Depends(get_message),
	create_comment: CreateComment = Depends(get_create_comment)
):
	command = CreateCommentCommand(author_id=user.id, theme_id=theme.id, section_id=section.id, content_id=content.id, **request.model_dump())
	message_id = await create_comment.execute(command)
	return v1_schemas.IdResponse(id=message_id)

@router.get("/{content_id}/comments", response_model=List[schemas.CommentMessageResponse])
async def get_comments_endpoint(
	user: UserDTO = Depends(get_current_user),
	content: MessageDTO = Depends(get_message),
	get_comments: GetComments = Depends(get_retrieve_comments),
	limit: int = Query(default=100, ge=1, le=1000),
	offset: int = Query(default=0, ge=0)
):
	query = GetCommentsQuery(theme_id=content.theme_id, section_id=content.section_id, content_id=content.id, limit=limit, offset=offset)
	comments = await get_comments.execute(query)
	return [schemas.CommentMessageResponse.model_validate(comment.model_dump()) for comment in comments]

@router.get("/comments/{id}", response_model=schemas.CommentMessageResponse)
async def get_comment_endpoint(
	user: UserDTO = Depends(get_current_user),
	comment: MessageDTO = Depends(get_comment),
):
	return schemas.CommentMessageResponse.model_validate(comment.model_dump())


@router.patch(
	"/{message_id}/reaction",
	response_model=schemas.MessageReactionResponse,
	responses={
		201: {"model": schemas.MessageReactionResponse},
		204: {"description": "Deleted successfully"}
	},
	summary="Upsert reaction",
	description="""
	Установить, изменить или удалить реакцию на сообщение.

	- Отправьте reaction=<MessageReactionTypeAPI> чтобы поставить или изменить реакцию
	- Отправьте reaction=null чтобы удалить реакцию

	Один пользователь может иметь только одну реакцию на сообщение.
	"""
)
async def upsert_message_reaction_endpoint(
	request: schemas.UpsertMessageReactionRequest,
	user: UserDTO = Depends(get_current_user),
	message: MessageDTO = Depends(get_message),
	upsert_message_reaction: UpsertMessageReaction = Depends(get_upsert_message_reaction)
):
	command = UpsertMessageReactionCommand(user_id=user.id, message_id=message.id, **request.model_dump())
	message_reaction = await upsert_message_reaction.execute(command)

	if not message_reaction:
		return Response(status_code=204)

	return schemas.MessageReactionResponse.model_validate(message_reaction.model_dump())

@router.get("/{message_id}/reaction", response_model=schemas.MessageReactionResponse)
async def get_message_reaction_endpoint(
	user: UserDTO = Depends(get_current_user),
	message: MessageDTO = Depends(get_message),
	get_message_reaction: GetMessageReaction = Depends(get_retrieve_message_reaction),
):
	command = GetMessageReactionQuery(user_id=user.id, message_id=message.id)
	message_reaction = await get_message_reaction.execute(command)

	return schemas.MessageReactionResponse.model_validate(message_reaction.model_dump())

@router.get("/{message_id}/reactions", response_model=schemas.MessageReactionStatsResponse)
async def get_message_reaction_stats_endpoint(
	user: UserDTO = Depends(get_current_user),
	message: MessageDTO = Depends(get_message),
	get_message_reaction_stats: GetMessageReactionStats = Depends(get_retrieve_message_reaction_stats),
):
	command = GetMessageReactionStatsQuery(message_id=message.id)
	message_reaction_stats = await get_message_reaction_stats.execute(command)

	return schemas.MessageReactionStatsResponse.model_validate(message_reaction_stats.model_dump())


# @router.post("/openai", response_model=OpenAIGenerateTextResponse)
# async def message_openai_generate_text_endpoint(
# 	data: OpenAIGenerateTextRequest,
# 	user: User = Depends(get_current_user),
# 	theme: Theme = Depends(get_theme),
# 	section: Section = Depends(get_theme_section),
# 	message_service: MessageService = Depends(get_message_service)
# ):
# 	openai_generate_text = await message_service.generate_text(data=data, user=user, theme=theme, section=section)
# 	return openai_generate_text_to_response(openai_generate_text=openai_generate_text)

