import jwt
from datetime import datetime, timedelta
from typing import Any

from src.core.config import settings
from src.domain.users.exceptions import TokenExpiredError, InvalidTokenError

class JWTManager:
	"""Менеджер JWT токенов"""
	@staticmethod
	def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
		"""Создать access token"""
		to_encode = data.copy()

		expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.jwt.access_token_expire_minutes))

		to_encode.update({"exp": expire, "type": "access"})
		encoded_jwt = jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)
		return encoded_jwt

	@staticmethod
	def create_refresh_token(user_id: Any) -> str:
		"""Создать refresh token"""
		expire = datetime.utcnow() + timedelta(days=settings.jwt.refresh_token_expire_days)
		to_encode = {"sub": str(user_id), "exp": expire, "type": "refresh"}
		return jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)

	@staticmethod
	def verify_token(token: str) -> dict:
		"""Верифицировать токен"""
		try:
			return jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm], options={"verify_exp": True})
		except jwt.ExpiredSignatureError:
			raise TokenExpiredError()
		except jwt.PyJWTError:
			raise InvalidTokenError()

	@staticmethod
	def extract_user_id_from_payload(payload: dict) -> str:
		"""Получить ID пользователя из токена"""
		user_id = payload.get("sub")
		if not user_id:
			raise InvalidTokenError("Token missing subject")
		return user_id

	@staticmethod
	def extract_provider_from_payload(payload: dict) -> str:
		"""Получить provider из токена"""
		provider = payload.get("provider")
		if not provider:
			raise InvalidTokenError("Token missing provider")
		return provider
