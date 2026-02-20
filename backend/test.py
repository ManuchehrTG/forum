from enum import Enum

class SectionTechVersionType(str, Enum):
	MINIMUM = "minimum"
	FULL = "full"

	@property
	def level(self) -> int:
		levels = {
			"minimum": 1,
			"full": 2,
		}
		return levels[self]

	def can_include(self, other: "SectionTechVersionType") -> bool:
		"""
		Бизнес-правило: может ли эта версия включать секции другой версии.
		Пример: FULL.can_include(MINIMUM) → True
		"""
		return other.level <= self.level

x = SectionTechVersionType.MINIMUM
other = SectionTechVersionType.FULL

print(x.can_include(other))
