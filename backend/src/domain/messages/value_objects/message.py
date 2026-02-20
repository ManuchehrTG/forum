from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import UUID

class MessageType(Enum):
	POST = "post"
	TASK = "task"
	TASK_ASSIGNMENT = "task_assignment"
	COMMENT = "comment"

class TaskAssignmentStatus(Enum):
	IN_PROGRESS = "in_progress"
	COMPLETED = "completed"
	CANCELLED = "cancelled"
	FAILED = "failed"

@dataclass(frozen=True)
class PostMessageData:
	"""Данные поста"""

	@classmethod
	def from_dict(cls, data: dict) -> "PostMessageData":
		return cls()

@dataclass(frozen=True)
class TaskMessageData:
	ratio: int

	def __post_init__(self):
		"""Валидация при создании"""
		if not (1 <= self.ratio <= 100):
			raise ValueError("Ratio должен быть от 1 до 100")

	@classmethod
	def from_dict(cls, data: dict) -> "TaskMessageData":
		return cls(ratio=data["ratio"])

@dataclass(frozen=True)
class TaskAssignmentMessageData:
	content_id: UUID
	expires_at: datetime
	is_partially: bool = False
	status: TaskAssignmentStatus = field(default=TaskAssignmentStatus.IN_PROGRESS)

	@classmethod
	def from_dict(cls, data: dict) -> "TaskAssignmentMessageData":
		return cls(
			content_id=data["content_id"],
			is_partially=data["is_partially"],
			status=data["status"],
			expires_at=data["expires_at"]
		)

@dataclass(frozen=True)  
class CommentMessageData:
	content_id: UUID
	reply_to_message_id: UUID | None = None

	@classmethod
	def from_dict(cls, data: dict) -> "CommentMessageData":
		return cls(
			content_id=data["content_id"],
			reply_to_message_id=data["reply_to_message_id"]
		)
