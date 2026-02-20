from typing import Tuple
from uuid import UUID

from src.domain.messages.value_objects import MessageType
from src.domain.sections.value_objects import SectionMessageType
from src.shared.exceptions.domain import NotFoundError, BusinessRuleError, UnprocessableEntityError

class SectionNotFoundError(NotFoundError):
	"""Секция не найдена"""
	error_code = "section_not_found"

	def __init__(self, section_id: str | UUID, search_type: str, **kwargs):
		super().__init__(entity="Section", entity_id=str(section_id), search_type=search_type, **kwargs)

	@classmethod
	def by_id(cls, section_id: str | UUID, **kwargs) -> "SectionNotFoundError":
		return cls(section_id=section_id, search_type="id", **kwargs)

	@classmethod
	def by_code(cls, section_code: str, **kwargs) -> "SectionNotFoundError":
		return cls(section_id=section_code, search_type="code", **kwargs)


class SectionMessageTypeConflictError(BusinessRuleError):
	"""Тип сообщения уже существует в разрешенных для секции"""
	error_code = "section_message_type_conflict"

	def __init__(self, message_type: MessageType, **kwargs):
		super().__init__(
			message=f"MessageType '{message_type.value}' already in section",
			**kwargs
		)


class CannotCommentOnCommentError(BusinessRuleError):
    """Нельзя комментировать комментарий"""
    error_code = "cannot_comment_on_comment"

    def __init__(self, message_id: str | UUID, **kwargs):
    	super().__init__(
    		message=f"Cannot comment on a comment message_id={message_id}",
    		details={"message_id": str(message_id)},
    		**kwargs
    	)


class SectionValidationError(UnprocessableEntityError):
	"""Логическая ошибка"""
	error_code = "section_validation"

	@classmethod
	def message_type_not_allowed(cls, message_type: MessageType, section_code: str, allowed_message_types: Tuple[SectionMessageType, ...], **kwargs):
		message_type_str = message_type.value

		return cls(
			message=f"MessageType '{message_type_str}' cannot be created for section '{section_code}'",
			code="section_validation.message_type_not_allowed",
			details={
				"message_type": message_type_str,
				"section_code": section_code,
				"allowed_message_types": [amt.to_dict() for amt in allowed_message_types],
				"reason": "message_type_not_allowed"
			},
			**kwargs
		)

	@classmethod
	def comments_not_allowed(cls, message_type: MessageType, section_code: str, allowed_message_types: Tuple[SectionMessageType, ...], **kwargs):
		message_type_str = message_type.value

		return cls(
			message=f"Comments cannot be created for MessageType '{message_type_str}' in section '{section_code}'",
			code="section_validation.comments_not_allowed",
			details={
				"message_type": message_type_str,
				"section_code": section_code,
				"allowed_message_types": [amt.to_dict() for amt in allowed_message_types],
				"reason": "comments_not_allowed"
			},
			**kwargs
		)
