import json
import hashlib
import hmac
from datetime import datetime, timedelta
from urllib.parse import parse_qsl, unquote

from app.core.config import settings
from infrastructure.logger import logger

"""
TODO:
	- Добавить проверку для verify_telegram, чтобы не переиспользовали initData
"""

def _is_auth_date_valid(auth_date: int, max_age_seconds: int):
	"""Проверка, что auth_date не старше N секунд"""
	auth_time = datetime.utcfromtimestamp(auth_date)
	now = datetime.utcnow()
	return (now - auth_time) <= timedelta(seconds=max_age_seconds)

def verify_telegram(init_data: str, max_age_seconds: int = settings.AUTH_DATE_EXPIRE_SECONDS) -> dict | None:
	"""Валидация initData подписи от Telegram WebApp."""
	try:
		parsed_data = dict(parse_qsl(init_data))
		received_hash = parsed_data.pop("hash", None)

		if not received_hash:
			return None

		# auth_date = int(parsed_data.get("auth_date", 0))
		# if not _is_auth_date_valid(auth_date, max_age_seconds):
		# 	return None

		# Формируем строку для проверки
		data_check_string = "\n".join(
			f"{key}={value}"
			for key, value in sorted(parsed_data.items())
		)

		# Ключ на основе BOT_TOKEN
		secret_key = hmac.new(
			key="WebAppData".encode(),
			msg=settings.TELEGRAM_BOT_TOKEN.encode(),
			digestmod=hashlib.sha256
		).digest()

		# Сравниваем хеши
		computed_hash = hmac.new(
			key=secret_key,
			msg=data_check_string.encode(),
			digestmod=hashlib.sha256
		).hexdigest()

		if not hmac.compare_digest(received_hash, computed_hash):
		# if not computed_hash == received_hash:
			return None

		user_str = unquote(parsed_data["user"])
		user_data = json.loads(user_str)

		return user_data
	except Exception as e:
		logger.warning(f"Invalid Telegram data format: {e}")
