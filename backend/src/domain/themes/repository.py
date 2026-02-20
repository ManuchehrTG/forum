from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.themes.entities import Theme

class ThemeRepository(ABC):
	"""Интерфейс репозитория тем"""
	@abstractmethod
	async def get_by_id(self, theme_id: UUID) -> Theme:
		pass

	@abstractmethod
	async def get_by_title(self, title: str) -> Theme:
		pass

	@abstractmethod
	async def get_root(self, system_user_id: UUID) -> Theme:
		pass

	@abstractmethod
	async def save(self, theme: Theme) -> None:
		pass
