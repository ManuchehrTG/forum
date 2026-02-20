from datetime import datetime
from typing import List, Tuple
from uuid import UUID, uuid4

from src.domain.messages.value_objects import MessageType
from src.domain.sections.exceptions import CannotCommentOnCommentError, SectionMessageTypeConflictError, SectionValidationError
from src.domain.sections.value_objects import TechVersionType, SectionMessageType

class Section:
	def __init__(
		self,
		code: str,
		tech_version: TechVersionType,
		id: UUID | None = None,
		openai_prompt: str | None = None,
		enable_openai: bool = True,
		allow_hide: bool = True,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
		allowed_message_types: List[SectionMessageType] | None = None
	):
		self.id = id or uuid4()
		self.code = code
		self.openai_prompt = openai_prompt
		self.tech_version = tech_version
		self.enable_openai = enable_openai
		self.allow_hide = allow_hide

		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

		self._allowed_message_types = allowed_message_types or []

	@property
	def allowed_message_types(self) -> Tuple[SectionMessageType, ...]:
		return tuple(self._allowed_message_types)

	def _touch(self):
		self.updated_at = datetime.utcnow()

	def has_allowed_message_type(self, message_type: MessageType) -> bool:
		return any(message_type == amt.message_type for amt in self._allowed_message_types)

	def has_allowed_comment_for_message_type(self, message_type: MessageType) -> bool:
		return any(message_type == amt.message_type for amt in self._allowed_message_types if amt.allow_comments is True)

	def add_allowed_message_type(self, message_type: MessageType, allow_comments: bool) -> None:
		if self.has_allowed_message_type(message_type):
			raise SectionMessageTypeConflictError(message_type)

		section_message_type = SectionMessageType(message_type=message_type, allow_comments=allow_comments)
		self._allowed_message_types.append(section_message_type)

		self._touch()

	def ensure_allowed_message_type(self, message_type: MessageType):
		if not self.has_allowed_message_type(message_type):
			raise SectionValidationError.message_type_not_allowed(message_type, self.code, self.allowed_message_types)

	def ensure_allowed_comment_for_message_type(self, message_type: MessageType):
		if message_type == MessageType.COMMENT:
			raise CannotCommentOnCommentError(f"Cannot comment on {message_type.value}")

		if not self.has_allowed_comment_for_message_type(message_type):
			raise SectionValidationError.comments_not_allowed(message_type, self.code, self.allowed_message_types)

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			code=record["code"],
			openai_prompt=record["openai_prompt"],
			tech_version=TechVersionType(record["tech_version"]),
			enable_openai=record["enable_openai"],
			allow_hide=record["allow_hide"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	@classmethod
	def from_db_with_allowed_message_types(cls, section_record: dict, section_message_type_records: List[dict]):
		section = cls.from_db_record(section_record)
		section._allowed_message_types = [SectionMessageType.from_db_record(record) for record in section_message_type_records]
		return section
