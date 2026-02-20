from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from .entities import Section

class SectionRepository(ABC):
	"""Интерфейс репозитория тем"""
	@abstractmethod
	async def get_by_id(self, section_id: UUID) -> Section:
		pass

	@abstractmethod
	async def get_by_code(self, section_code: str) -> Section:
		pass

	@abstractmethod
	async def get_list(self) -> List[Section]:
		pass

	@abstractmethod
	async def save(self, section: Section) -> None:
		pass
