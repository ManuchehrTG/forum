from asyncpg import Pool
from fastapi import Depends
from uuid import UUID

from src.api.dependencies import get_db_pool
from src.api.v1.media_files.dependencies import get_media_file_repository, get_storage_service
from src.api.v1.sections.dependencies import get_section_repository
from src.application.message_reactions.use_cases.get import GetMessageReaction
from src.application.message_reactions.use_cases.get_stats import GetMessageReactionStats
from src.application.message_reactions.use_cases.upsert import UpsertMessageReaction
from src.application.messages.dtos import MessageDTO
from src.application.messages.queries import GetCommentQuery, GetMessageQuery, GetPostQuery, GetTaskAssignmentQuery, GetTaskQuery
from src.application.messages.services.media_attachment import MessageMediaAttachmentService
from src.application.messages.use_cases.create_comment import CreateComment
from src.application.messages.use_cases.create_post import CreatePost
from src.application.messages.use_cases.create_task import CreateTask
from src.application.messages.use_cases.create_task_assignment import CreateTaskAssignment
from src.application.messages.use_cases.get import GetMessage
from src.application.messages.use_cases.get_comment import GetComment
from src.application.messages.use_cases.get_comments import GetComments
from src.application.messages.use_cases.get_post import GetPost
from src.application.messages.use_cases.get_posts import GetPosts
from src.application.messages.use_cases.get_task import GetTask
from src.application.messages.use_cases.get_task_assignment import GetTaskAssignment
from src.application.messages.use_cases.get_task_assignments import GetTaskAssignments
from src.application.messages.use_cases.get_tasks import GetTasks
from src.domain.media_files.repository import MediaFileRepository
from src.domain.message_reactions.repository import MessageReactionRepository
from src.domain.messages.repository import MessageRepository
from src.domain.sections.repository import SectionRepository
from src.domain.interfaces.storage_service import StorageService
from src.infrastructure.database.repositories.raw_sql.messages import RawSQLMessageRepository
from src.infrastructure.database.repositories.raw_sql.message_reactions import RawSQLMessageReactionRepository

async def get_message_repository(
	pool: Pool = Depends(get_db_pool)
) -> MessageRepository:
	return RawSQLMessageRepository(pool)

async def get_message_media_attachment_service(
	storage_service: StorageService = Depends(get_storage_service)
):
	return MessageMediaAttachmentService(storage_service)

async def get_create_post(
	message_repo: MessageRepository = Depends(get_message_repository),
	section_repo: SectionRepository = Depends(get_section_repository),
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	media_attachment_service: MessageMediaAttachmentService = Depends(get_message_media_attachment_service)
) -> CreatePost:
	return CreatePost(message_repo, section_repo, media_file_repo, media_attachment_service)

async def get_create_task(
	message_repo: MessageRepository = Depends(get_message_repository),
	section_repo: SectionRepository = Depends(get_section_repository),
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	media_attachment_service: MessageMediaAttachmentService = Depends(get_message_media_attachment_service)
) -> CreateTask:
	return CreateTask(message_repo, section_repo, media_file_repo, media_attachment_service)

async def get_create_task_assignment(
	message_repo: MessageRepository = Depends(get_message_repository),
	section_repo: SectionRepository = Depends(get_section_repository),
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	media_attachment_service: MessageMediaAttachmentService = Depends(get_message_media_attachment_service)
) -> CreateTaskAssignment:
	return CreateTaskAssignment(message_repo, section_repo, media_file_repo, media_attachment_service)

async def get_create_comment(
	message_repo: MessageRepository = Depends(get_message_repository),
	section_repo: SectionRepository = Depends(get_section_repository),
	media_file_repo: MediaFileRepository = Depends(get_media_file_repository),
	media_attachment_service: MessageMediaAttachmentService = Depends(get_message_media_attachment_service)
) -> CreateComment:
	return CreateComment(message_repo, section_repo, media_file_repo, media_attachment_service)


async def get_retrieve_message(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetMessage:
	return GetMessage(message_repo)


async def get_retrieve_post(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetPost:
	return GetPost(message_repo)

async def get_retrieve_task(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetTask:
	return GetTask(message_repo)

async def get_retrieve_task_assignment(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetTaskAssignment:
	return GetTaskAssignment(message_repo)

async def get_retrieve_comment(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetComment:
	return GetComment(message_repo)


async def get_retrieve_posts(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetPosts:
	return GetPosts(message_repo)

async def get_retrieve_tasks(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetTasks:
	return GetTasks(message_repo)

async def get_retrieve_task_assignments(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetTaskAssignments:
	return GetTaskAssignments(message_repo)

async def get_retrieve_comments(
	message_repo: MessageRepository = Depends(get_message_repository)
) -> GetComments:
	return GetComments(message_repo)


async def get_message(
	message_id: UUID,
	get_message: GetMessage = Depends(get_retrieve_message)
) -> MessageDTO:
	query = GetMessageQuery(message_id=message_id)
	return await get_message.execute(query)


async def get_post(
	post_id: UUID,
	get_post: GetPost = Depends(get_retrieve_post)
) -> MessageDTO:
	query = GetPostQuery(post_id=post_id)
	return await get_post.execute(query)

async def get_task(
	task_id: UUID,
	get_task: GetTask = Depends(get_retrieve_task)
) -> MessageDTO:
	query = GetTaskQuery(task_id=task_id)
	return await get_task.execute(query)

async def get_task_assignment(
	task_assignment_id: UUID,
	get_task_assignment: GetTaskAssignment = Depends(get_retrieve_task_assignment)
) -> MessageDTO:
	query = GetTaskAssignmentQuery(task_assignment_id=task_assignment_id)
	return await get_task_assignment.execute(query)

async def get_comment(
	comment_id: UUID,
	get_comment: GetComment = Depends(get_retrieve_comment)
) -> MessageDTO:
	query = GetCommentQuery(comment_id=comment_id)
	return await get_comment.execute(query)



async def get_message_reaction_repository(
	pool: Pool = Depends(get_db_pool)
) -> MessageReactionRepository:
	return RawSQLMessageReactionRepository(pool)

async def get_upsert_message_reaction(
	message_reaction_repo: MessageReactionRepository = Depends(get_message_reaction_repository)
) -> UpsertMessageReaction:
	return UpsertMessageReaction(message_reaction_repo)

async def get_retrieve_message_reaction(
	message_reaction_repo: MessageReactionRepository = Depends(get_message_reaction_repository)
) -> GetMessageReaction:
	return GetMessageReaction(message_reaction_repo)

async def get_retrieve_message_reaction_stats(
	message_reaction_repo: MessageReactionRepository = Depends(get_message_reaction_repository)
) -> GetMessageReactionStats:
	return GetMessageReactionStats(message_reaction_repo)
