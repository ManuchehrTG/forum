import uuid
from abc import ABC, abstractmethod

from .value_objects import AuthProviderType

class AvatarDownloader(ABC):
	"""Абстракция для загрузки аватаров пользователей"""

	@abstractmethod
	async def download(self, provider: AuthProviderType, photo_url: str, user_id: uuid.UUID) -> str | None:
		"""Загружает аватар из внешнего источника"""
		pass
