import re
from dataclasses import dataclass
from enum import Enum

class AuthProviderType(Enum):
	TELEGRAM = "telegram"

@dataclass(frozen=True)
class Email:
	"""Value Object для Email"""

	value: str

	def __post_init__(self):
		if self.value:  # Валидируем только если не пустой
			self._validate()

	def _validate(self):
		"""Валидация email"""
		if "@" not in self.value:
			raise ValueError("Invalid email format")
		if "." not in self.value.split("@")[1]:
			raise ValueError("Invalid email domain")

	@classmethod
	def empty(cls):
		return cls("")

	@property
	def is_empty(self) -> bool:
		return self.value == ""

	def __str__(self):
		return self.value

@dataclass(frozen=True)
class Phone:
	"""Value Object для номера телефона"""
	value: str

	def __post_init__(self):
		if self.value:
			self._normalize()
			self._validate()

	def _normalize(self):
		"""Нормализовать номер телефона"""
		# Убираем все нецифровые символы
		normalized = re.sub(r'\D', '', self.value)
		# Меняем value через object.__setattr__ (т.к. frozen)
		object.__setattr__(self, 'value', normalized)

	def _validate(self):
		"""Валидация номера телефона"""
		if not self.value.isdigit():
			raise ValueError("Phone must contain only digits")
		if len(self.value) < 10:
			raise ValueError("Phone number too short")
		if len(self.value) > 15:
			raise ValueError("Phone number too long")

	@classmethod
	def empty(cls):
		return cls("")

	@property
	def is_empty(self) -> bool:
		return self.value == ""

	def __str__(self):
		return self.value

	def __bool__(self):
		return not self.is_empty
