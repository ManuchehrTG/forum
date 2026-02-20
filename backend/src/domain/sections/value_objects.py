from enum import Enum

from src.domain.messages.value_objects import MessageType

class TechVersionType(Enum):
	MINIMUM = "minimum"
	FULL = "full"

	@property
	def level(self) -> int:
		levels = {
			"minimum": 1,
			"full": 2,
		}
		return levels[self.value]

	def can_include(self, other: "TechVersionType") -> bool:
		"""
		Бизнес-правило: может ли эта версия включать секции другой версии.
		Пример: FULL.can_include(MINIMUM) → True
		"""
		return self.level >= other.level


class SectionMessageType:
	def __init__(
		self,
		message_type: MessageType,
		allow_comments: bool,
	):
		self.message_type = message_type
		self.allow_comments = allow_comments

	def to_dict(self) -> dict:
		return {
			"message_type": self.message_type.value,
			"allow_comments": self.allow_comments
		}

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			message_type=MessageType(record["message_type"]),
			allow_comments=record["allow_comments"],
		)

