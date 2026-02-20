from pydantic import BaseModel
from uuid import UUID

# GET
class GetMessageQuery(BaseModel):
	"""Query для получения сообщения"""
	message_id: UUID

class GetPostQuery(BaseModel):
	"""Query для получения поста"""
	post_id: UUID

class GetTaskQuery(BaseModel):
	"""Query для получения задачи"""
	task_id: UUID

class GetTaskAssignmentQuery(BaseModel):
	"""Query для получения назачения задачи"""
	task_assignment_id: UUID

class GetCommentQuery(BaseModel):
	"""Query для получения комментария"""
	comment_id: UUID

# GETs
class BaseGetListQuery(BaseModel):
	"""Базовый Query для получения сообщений"""
	limit: int
	offset: int
	theme_id: UUID
	section_id: UUID

class GetPostsQuery(BaseGetListQuery):
	"""Query для получения постов"""
	pass

class GetTasksQuery(BaseGetListQuery):
	"""Query для получения задач"""
	pass

class GetTaskAssignmentsQuery(BaseGetListQuery):
	"""Query для получения назначений задачи"""
	content_id: UUID

class GetCommentsQuery(BaseGetListQuery):
	"""Query для получения комментариев"""
	content_id: UUID
