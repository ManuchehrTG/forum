from typing import Dict
import uuid
from pathlib import Path

from src.core.config import settings
from src.domain.users.avatar_downloader import AvatarDownloader, AuthProviderType
from src.infrastructure.logger import logger
from .telegram import TelegramAvatarDownloader

class CompositeAvatarDownloader(AvatarDownloader):
	"""Объединяет загрузчики для разных провайдеров"""

	def __init__(self, avatar_dir: str = settings.storage.avatar_dir):
		self.avatar_dir = Path(avatar_dir)
		self._downloaders: Dict[AuthProviderType, AvatarDownloader] = {}
		self._register_defaults()

	def _register_defaults(self):
		"""Регистрирует дефолтные загрузчики"""
		self.register(AuthProviderType.TELEGRAM, TelegramAvatarDownloader(str(self.avatar_dir)))

	def register(self, provider: AuthProviderType, downloader: AvatarDownloader):
		"""Регистрирует загрузчик для провайдера"""
		self._downloaders[provider] = downloader

	async def download(self, provider: AuthProviderType, photo_url: str, user_id: uuid.UUID) -> str | None:
		"""Делегирует загрузку соответствующему загрузчику"""
		downloader = self._downloaders.get(provider)
		if not downloader:
			logger.warning(f"No downloader registered for provider: {provider}")
			return None

		return await downloader.download(provider, photo_url, user_id)

# Фабричная функция
def create_avatar_downloader() -> AvatarDownloader:
	"""Создает и конфигурирует загрузчик аватаров"""
	return CompositeAvatarDownloader()
