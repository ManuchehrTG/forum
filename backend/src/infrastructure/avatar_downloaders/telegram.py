import aiofiles
import httpx
import uuid
from pathlib import Path

from src.core.config import settings
from src.domain.users.value_objects import AuthProviderType
from src.domain.users.avatar_downloader import AvatarDownloader
from src.infrastructure.logger import logger

class TelegramAvatarDownloader(AvatarDownloader):
	def __init__(self, avatar_dir: str | None = None):
		self.avatar_dir = Path(avatar_dir or settings.storage.avatar_dir)
		self.avatar_dir.mkdir(parents=True, exist_ok=True)

	async def download(self, provider: AuthProviderType, photo_url: str, user_id: uuid.UUID) -> str | None:
		"""Загрузка аватара из Telegram"""
		if provider != AuthProviderType.TELEGRAM:
			return None

		async with httpx.AsyncClient(follow_redirects=True) as client:
			try:
				response = await client.get(photo_url)
				response.raise_for_status()
			except httpx.HTTPStatusError as e:
				logger.warning(f"Telegram avatar download failed: {e}")
				return None
			except httpx.RequestError as e:
				logger.warning(f"Telegram avatar request failed: {e}")
				return None

		content_type = response.headers.get("Content-Type", "")
		if content_type == "image/svg+xml":
			return None

		# Сохраняем в пользовательскую директорию
		user_dir = self.avatar_dir / str(user_id)
		user_dir.mkdir(exist_ok=True)
		
		file_name = f"{uuid.uuid4()}.jpg"
		file_path = user_dir / file_name

		async with aiofiles.open(file_path, "wb") as f:
			await f.write(response.content)

		return str(file_path)
