from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.users.entities import User
from src.domain.users.value_objects import AuthProviderType

class UserRepository(ABC):
	"""Интерфейс репозитория пользователей"""
	@abstractmethod
	async def get_by_id(self, user_id: UUID) -> User:
		pass

	@abstractmethod
	async def get_by_provider_user_id(self, provider: AuthProviderType, provider_user_id: str) -> User:
		pass

	@abstractmethod
	async def add(self, user: User) -> None:
		pass

	@abstractmethod
	async def update(self, user: User) -> None:
		pass

	@abstractmethod
	async def set_avatar(self, user_id: UUID, avatar_path: str) -> None:
		pass
