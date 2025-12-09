import asyncio
import aiofiles
import httpx

from pathlib import Path

from app.core.config import settings

async def download_telegram_avatar(
	photo_url: str,
	user_id: int,
	subdir: str = "avatars",
	timeout: float = 10.0,
	retries: int = 2,
	overwrite: bool = True
) -> str:
	"""
	Скачивает аватар Telegram с улучшенной обработкой ошибок и безопасностью.

	Args:
		photo_url: URL аватарки из Telegram
		user_id: ID пользователя для имени файла
		subdir: Поддиректория для хранения (относительно STORAGE_DIR)
		timeout: Таймаут загрузки в секундах
		retries: Количество попыток перезагрузки при ошибках

	Returns:
		Относительный путь к сохранённому файлу (например "avatars/12/12345.jpg")
		или "default.jpg" при ошибке.
	"""
	user_prefix = str(user_id)[:2].zfill(2)
	storage_path = Path(settings.STORAGE_DIR).absolute()
	save_dir = storage_path / subdir / user_prefix
	save_dir.mkdir(parents=True, exist_ok=True)

	for attempt in range(retries + 1):
		try:
			async with httpx.AsyncClient(timeout=timeout) as client:
				response = await client.get(photo_url, follow_redirects=True)

				content = await response.aread()

				content_type = response.headers.get("content-type", "").lower()
				if not content_type.startswith("image/"):
					print(f"Invalid content type: {content_type}")
					return None
					# raise ValueError(f"Invalid content type: {content_type}")

				# Определение расширения
				ext = Path(response.url.path).suffix.lower()
				if not ext:
					if "webp" in content_type:
						ext = ".webp"
					elif "png" in content_type:
						ext = ".png"
					elif "jpeg" in content_type or "jpg" in content_type:
						ext = ".jpg"
					else:
						ext = ".dat"  # Фолбэк для неизвестных типов

				filename = f"{user_id}{ext}"
				filepath = save_dir / filename

				if filepath.exists() and not overwrite:
					return {
						"relative_path": filepath.relative_to(storage_path / subdir).as_posix(),
						"abs_path": filepath.as_posix()
					}

				# Атомарная запись во временный файл
				temp_path = filepath.with_suffix('.tmp')

				try:
					async with aiofiles.open(temp_path, "wb") as f:
						await f.write(content)

					# Windows требует удаления целевого файла перед переименованием
					if filepath.exists():
						filepath.unlink()

					# Переименовываем после успешной записи
					temp_path.rename(filepath)

					return {
						"relative_path": filepath.relative_to(storage_path / subdir).as_posix(),
						"abs_path": filepath.as_posix()
					}
				except Exception as e:
					if temp_path.exists():
						temp_path.unlink()
					raise

		except Exception as e:
			if attempt == retries:
				print(f"Avatar download failed after {retries} attempts: {e}")
				return None
			await asyncio.sleep(1 * (attempt + 1))  # Экспоненциальная задержка
