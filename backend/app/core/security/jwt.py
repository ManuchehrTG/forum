import jwt
from datetime import datetime, timedelta
from typing import Any, Dict

from app.core.config import settings
from app.domains.auth.exceptions import InvalidTokenError, TokenExpiredError

def create_access_token(payload_data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
	"""Создает новый JWT токен с указанными данными.

	Args:
		payload_data: Данные для включения в токен.
		expires_delta: Время жизни токена. Если не указано, используется дефолтное.

	Returns:
		Строка с JWT токеном.
	"""
	payload = payload_data.copy()
	expire_time = datetime.utcnow() + (expires_delta or timedelta(seconds=settings.JWT_TOKEN_EXPIRE_SECONDS))
	payload["exp"] = expire_time

	return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_jwt(token: str) -> Dict[str, Any] | None:
	try:
		if token.startswith("Bearer "):
			token = token[7:]

		payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

		# if _should_refresh_token(payload=payload):
		# 	new_token = create_access_token(payload_data=payload)

		return payload

	except jwt.ExpiredSignatureError:
		raise TokenExpiredError()
	except (jwt.PyJWTError, jwt.DecodeError, jwt.InvalidSignatureError, jwt.InvalidTokenError) as e:
		raise InvalidTokenError()

def _should_refresh_token(payload: Dict[str, Any]) -> bool:
	"""Определяет, нужно ли обновлять токен.

	Токен обновляется, если до истечения срока осталось меньше
	`JWT_TOKEN_GRACE_PERIOD_FOR_RENEWAL_SECONDS`.
	"""
	expiration_time = datetime.utcfromtimestamp(payload["exp"])
	time_remaining = expiration_time - datetime.utcnow()

	return time_remaining <= timedelta(seconds=settings.JWT_TOKEN_GRACE_PERIOD_FOR_RENEWAL_SECONDS)
