from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from uuid import UUID

from src.domain.messages.value_objects import MessageType, TaskAssignmentStatus

class MessageMediaFileDTO(BaseModel):
	media_file_id: UUID
	sort_order: int

class MessageDTO(BaseModel):
	"""DTO для передачи данных агрегата Message между слоями"""
	id: UUID
	author_id: UUID
	theme_id: UUID
	section_id: UUID
	type: MessageType
	text: str | None
	is_openai_generated: bool
	created_at: datetime
	updated_at: datetime

	# Для TASK:
	ratio: int | None = None

	# Для TASK_ASSIGNMENT:
	content_id: UUID | None = None # Также для Comment
	is_partially: bool | None = None
	status: TaskAssignmentStatus | None = None
	expires_at: datetime | None = None

	# Для COMMENT:
	reply_to_message_id: UUID | None = None

	media_files: List[MessageMediaFileDTO] = Field(default_factory=list)

class MessageImproveTextDTO(BaseModel):
	input_text: str
	output_text: str | None
