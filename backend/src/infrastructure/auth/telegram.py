import json
import hmac
import hashlib
from pydantic import BaseModel
from urllib.parse import parse_qsl

from src.core.config import settings

class TelegramUserData(BaseModel):
	id: int
	first_name: str
	last_name: str | None
	username: str | None
	language_code: str | None
	photo_url: str | None


class TelegramInitDataValidator:
	def validate(self, init_data: str) -> TelegramUserData:
		data = dict(parse_qsl(init_data, strict_parsing=True))

		hash_ = data.pop("hash", None)
		if not hash_:
			raise ValueError("Missing 'hash' field in init_data")

		check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

		secret_key = hmac.new(
			key=b"WebAppData",
			msg=settings.telegram_bot.token.encode(),
			digestmod=hashlib.sha256,
		).digest()

		expected_hash = hmac.new(
			secret_key,
			check_string.encode(),
			hashlib.sha256,
		).hexdigest()

		if not hmac.compare_digest(hash_, expected_hash):
			raise ValueError("Invalid initData signature (hash)")

		user = data.get("user")
		if not user:
			raise ValueError("Missing user")

		user = json.loads(user)

		return TelegramUserData(
			id=user["id"],
			first_name=user["first_name"],
			last_name=user.get("last_name"),
			username=user.get("username"),
			language_code=user.get("language_code"),
			photo_url=user.get("photo_url"),
		)
