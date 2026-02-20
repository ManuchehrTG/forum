from datetime import datetime
from typing import List
from uuid import UUID

from src.domain.messages.value_objects import MessageType
from src.shared.exceptions import NotFoundError, BusinessRuleError, UnprocessableEntityError

class MessageNotFoundError(NotFoundError):
	"""Сообщение не найдено"""
	error_code = "message_not_found"

	def __init__(self, message_id: str | UUID, search_type: str, entity: str = "Message", **kwargs):
		super().__init__(entity=entity, entity_id=str(message_id), search_type=search_type, **kwargs)

	@classmethod
	def by_id(cls, message_id: str | UUID, **kwargs) -> "MessageNotFoundError":
		return cls(message_id=message_id, search_type="id", **kwargs)

	@classmethod
	def by_id_and_type(cls, message_id: str | UUID, message_type: MessageType, **kwargs) -> "MessageNotFoundError":
		"""Сообщение определенного типа не найдено"""
		return cls(
			message_id=message_id,
			search_type=f"id and type '{message_type}'",
			entity=f"Message ({message_type})",
			**kwargs
		)

class MessageStateConflictError(BusinessRuleError):
	"""Сообщение в неправильном состоянии для операции"""
	error_code = "message_state_conflict"

	@classmethod
	def expected_type(cls, message_id: str | UUID, actual: MessageType, expected: MessageType, **kwargs):
		return cls(
			message=f"Message {message_id} is {actual.value}, expected {expected.value}",
			code="message_state_conflict.expected_type",
			details={
				"message_id": str(message_id),
				"actual_type": actual.value,
				"expected_type": expected.value,
				"reason": "wrong_message_type"
			},
			**kwargs
		)


class MessageContentMismatchError(BusinessRuleError):
	"""Сообщение ссылается на другой контент"""
	error_code = "message_content_mismatch"

	def __init__(self, message_type: MessageType, message_id: str | UUID, expected: str | UUID, actual: str | UUID, **kwargs):
		super().__init__(
			message=f"{message_type.value} '{message_id}' is linked to content '{actual}', expected '{expected}'",
			details={
				"message_type": message_type.value,
				"message_id": str(message_id),
				"expected_content_id": str(expected),
				"actual_content_id": str(actual)
			},
			**kwargs
		)


class TaskValidationError(UnprocessableEntityError):
	"""Ошибка валидации параметров задачи"""
	error_code = "task_validation"

	@classmethod
	def deadline_too_soon(cls, expires_at: datetime, min_days: int = 1, **kwargs):
		return cls(
			message=f"Deadline {expires_at.date()} is too soon. Minimum {min_days} day from now",
			code="task_validation.deadline_too_soon",
			details={
				"expires_at": expires_at.isoformat(),
				"min_days": min_days,
				"reason": "deadline_too_soon"
			},
			**kwargs
		)

	@classmethod
	def deadline_too_far(cls, expires_at: datetime, max_days: int = 30, **kwargs):
		return cls(
			message=f"Deadline {expires_at.date()} is too far. Maximum {max_days} days from now",
			code="task_validation.deadline_too_far",
			details={
				"expires_at": expires_at.isoformat(),
				"max_days": max_days,
				"reason": "deadline_too_far"
			},
			**kwargs
		)

class MessageMediaFileConflictError(BusinessRuleError):
	"""Медиафайл сообщения уже существует"""
	error_code = "message_media_file_conflict"

	def __init__(self, media_file_id: str | UUID, **kwargs):
		message = f"MediaFile {media_file_id} already in message"
		details = {"media_file_id": str(media_file_id)}
		super().__init__(message, details=details, **kwargs)


class MessageEmptyFieldError(UnprocessableEntityError):
	"""Сообщение не может быть пустым"""
	error_code = "message_empty_field"

	def __init__(self, message_type: MessageType, required_fields: List[str], **kwargs):
		required_fields_str = ",".join(required_fields)
		message = f"{message_type.value} must contain at least one of: {required_fields_str}"
		details = {
			"message_type": message_type.value,
			"required_fields": required_fields,
			"hint": f"Provide at least one of these {required_fields_str}"
		}
		super().__init__(message, details=details, **kwargs)

	@classmethod
	def post(cls, required_fields: List[str]):
		return cls(
			message_type=MessageType.POST,
			required_fields=required_fields,
		)

	@classmethod
	def comment(cls, required_fields: List[str]):
		return cls(
			message_type=MessageType.COMMENT,
			required_fields=required_fields,
		)
