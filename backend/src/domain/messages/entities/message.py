import json
from datetime import UTC, datetime, timedelta
from typing import List, Tuple
from uuid import UUID, uuid4

from src.domain.messages.exceptions import MessageContentMismatchError, MessageEmptyFieldError, MessageMediaFileConflictError, MessageStateConflictError, TaskValidationError
from src.domain.messages.value_objects import MessageType, PostMessageData, TaskMessageData, TaskAssignmentMessageData, CommentMessageData, MessageMediaFile

class Message:
	"""Агрегат Message - корневая сущность"""
	def __init__(
		self,
		id: UUID,
		author_id: UUID,
		theme_id: UUID,
		section_id: UUID,
		type: MessageType,
		text: str | None,
		is_openai_generated: bool,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
		post_data: PostMessageData | None = None,
		task_data: TaskMessageData | None = None,
		task_assignment_data: TaskAssignmentMessageData | None = None,
		comment_data: CommentMessageData | None = None,
		media_files: List[MessageMediaFile] | None = None,
	):
		self.id = id
		self.author_id = author_id
		self.theme_id = theme_id
		self.section_id = section_id
		self.type = type
		self.text = text
		self.is_openai_generated = is_openai_generated
		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or self.created_at

		self.post_data = post_data
		self.task_data = task_data
		self.task_assignment_data = task_assignment_data
		self.comment_data = comment_data

		self._media_files = media_files or []

	@property
	def media_files(self) -> Tuple[MessageMediaFile, ...]:
		return tuple(self._media_files)

	def __post_init__(self):
		"""Проверяем инварианты"""

		# Проверяем что данные соответствуют типу
		if self.type == MessageType.POST and not self.post_data:
			raise ValueError("POST message must have post_data")
		if self.type == MessageType.TASK and not self.task_data:
			raise ValueError("TASK message must have task_data")
		if self.type == MessageType.TASK_ASSIGNMENT and not self.task_assignment_data:
			raise ValueError("TASK_ASSIGNMENT message must have task_assignment_data")
		if self.type == MessageType.COMMENT and not self.comment_data:
			raise ValueError("COMMENT message must have comment_data")

		# Проверяем что нет лишних данных
		if self.type != MessageType.POST and self.post_data:
			raise ValueError(f"Non-POST message cannot have post_data")
		if self.type != MessageType.TASK and self.task_data:
			raise ValueError(f"Non-TASK message cannot have task_data")
		if self.type != MessageType.TASK_ASSIGNMENT and self.task_assignment_data:
			raise ValueError(f"Non-TASK_ASSIGNMENT message cannot have task_assignment_data")
		if self.type != MessageType.COMMENT and self.comment_data:
			raise ValueError(f"Non-COMMENT message cannot have comment_data")

	def _touch(self):
		self.updated_at = datetime.utcnow()

	def _ensure_type(self, expected: MessageType) -> None:
		"""Бизнес-правило: проверка что это ожидаемый MessageType"""
		if self.type != expected:
			raise MessageStateConflictError.expected_type(message_id=self.id, actual=self.type, expected=expected)

	def ensure_is_post(self) -> None:
		self._ensure_type(MessageType.POST)

	def ensure_is_task(self) -> None:
		self._ensure_type(MessageType.TASK)

	def ensure_is_task_assignment(self) -> None:
		self._ensure_type(MessageType.TASK_ASSIGNMENT)

	def ensure_is_comment(self) -> None:
		self._ensure_type(MessageType.COMMENT)

	def ensure_content(self, content_id: UUID) -> None:
		if self.type == MessageType.TASK_ASSIGNMENT and self.task_assignment_data:
			if not self.task_assignment_data.content_id == content_id:
				raise MessageContentMismatchError(self.type, self.id, expected=content_id, actual=self.task_assignment_data.content_id)
		if self.type == MessageType.COMMENT and self.comment_data:
			if not self.comment_data.content_id == content_id:
				raise MessageContentMismatchError(self.type, self.id, expected=content_id, actual=self.comment_data.content_id)

	def ensure_required_fields(self) -> None:
		if self.type == MessageType.POST:
			if not (self.text or self._media_files):
				raise MessageEmptyFieldError.post(["text", "media_files"])
		if self.type == MessageType.COMMENT:
			if not (self.text or self._media_files):
				raise MessageEmptyFieldError.comment(["text", "media_files"])

	def has_media_file(self, media_file_id: UUID):
		return any(media_file_id == mf.media_file_id for mf in self._media_files)

	def add_media_file(self, media_file_id: UUID):
		if self.has_media_file(media_file_id):
			raise MessageMediaFileConflictError(media_file_id)

		sort_order = len(self._media_files) + 1
		message_media_file = MessageMediaFile(media_file_id=media_file_id, sort_order=sort_order)
		self._media_files.append(message_media_file)

		self._touch()

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			author_id=record["author_id"],
			theme_id=record["theme_id"],
			section_id=record["section_id"],
			type=MessageType(record["type"]),
			text=record["text"],
			is_openai_generated=record["is_openai_generated"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	@classmethod
	def from_db_record_with_data(cls, record: dict):
		message = cls.from_db_record(record)

		match message.type:
			case MessageType.POST:
				message.post_data = PostMessageData.from_dict(record["post_message_data"])
			case MessageType.TASK:
				message.task_data = TaskMessageData.from_dict(record["task_message_data"])
			case MessageType.TASK_ASSIGNMENT:
				message.task_assignment_data = TaskAssignmentMessageData.from_dict(record["task_assignment_message_data"])
			case MessageType.COMMENT:
				message.comment_data = CommentMessageData.from_dict(record["comment_message_data"])

		return message

	@classmethod
	def from_db_record_with_data_and_media(cls, record: dict):
		message = cls.from_db_record_with_data(record)
		message._media_files = [MessageMediaFile.from_db_record(record) for record in json.loads(record["message_media_files"])] if record.get("message_media_files") else []

		return message


	@classmethod
	def create_post(cls, author_id: UUID, theme_id: UUID, section_id: UUID, text: str | None, is_openai_generated: bool) -> "Message":
		"""Создать пост"""
		post_data = PostMessageData()

		message = cls(
			id=uuid4(),
			type=MessageType.POST,
			author_id=author_id,
			theme_id=theme_id,
			section_id=section_id,
			text=text,
			is_openai_generated=is_openai_generated,
			post_data=post_data
		)

		return message

	@classmethod
	def create_task(cls, author_id: UUID, theme_id: UUID, section_id: UUID, text: str, is_openai_generated: bool, ratio: int) -> "Message":
		"""Создать задачу"""
		task_data = TaskMessageData(ratio=ratio)

		message = cls(
			id=uuid4(),
			type=MessageType.TASK,
			author_id=author_id,
			theme_id=theme_id,
			section_id=section_id,
			text=text,
			is_openai_generated=is_openai_generated,
			task_data=task_data
		)

		return message

	@classmethod
	def create_task_assignment(
		cls,
		author_id: UUID,
		theme_id: UUID,
		section_id: UUID,
		text: str,
		is_openai_generated: bool,
		content_id: UUID,
		expires_at: datetime,
		is_partially: bool
	) -> "Message":
		"""Создать назначение задачи"""
		now = datetime.now(UTC)

		if expires_at < (now + timedelta(days=1)):
			raise TaskValidationError.deadline_too_soon(expires_at)

		if expires_at > (now + timedelta(days=30)):
			raise TaskValidationError.deadline_too_far(expires_at)

		task_assignment_data = TaskAssignmentMessageData(content_id=content_id, is_partially=is_partially, expires_at=expires_at)

		message = cls(
			id=uuid4(),
			type=MessageType.TASK_ASSIGNMENT,
			author_id=author_id,
			theme_id=theme_id,
			section_id=section_id,
			text=text,
			is_openai_generated=is_openai_generated,
			task_assignment_data=task_assignment_data
		)

		return message

	@classmethod
	def create_comment(
		cls,
		author_id: UUID,
		theme_id: UUID,
		section_id: UUID,
		text: str | None,
		is_openai_generated: bool,
		content_id: UUID,
		reply_to_message_id: UUID | None
	) -> "Message":
		"""Создать комментарий"""
		comment_data = CommentMessageData(content_id=content_id, reply_to_message_id=reply_to_message_id)

		message = cls(
			id=uuid4(),
			type=MessageType.COMMENT,
			author_id=author_id,
			theme_id=theme_id,
			section_id=section_id,
			text=text,
			is_openai_generated=is_openai_generated,
			comment_data=comment_data
		)

		return message
