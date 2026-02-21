from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class MessageReactionType(Enum):
	LIKE = "like"
	DISLIKE = "dislike"

@dataclass(frozen=True)
class MessageReactionStats:
	"""
	Value Object: Статистика реакций на сообщение
	"""
	reactions: Dict[MessageReactionType, int]

	@property
	def total(self) -> int:
		return sum(self.reactions.values())

	def to_dict(self) -> dict:
		return {
			"reactions": {reaction.value: count for reaction, count in self.reactions.items()},
			"total": self.total,
		}

	@classmethod
	def from_db_rows(cls, rows: List[dict]) -> "MessageReactionStats":
		return cls(
			reactions={MessageReactionType(row["reaction"]): row["count"] for row in rows}
		)
