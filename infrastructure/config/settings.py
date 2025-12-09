from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import computed_field
from typing import List

class InfrastructureSettings(BaseSettings):
	# Postgres
	DATABASE_HOST: str
	DATABASE_PORT: int
	DATABASE_USER: str
	DATABASE_PASSWORD: str
	DATABASE_NAME: str

	# Redis
	REDIS_HOST: str
	REDIS_PORT: int
	REDIS_DB: int
	REDIS_USERNAME: str | None = None
	REDIS_PASSWORD: str | None = None

	# HTTP
	# HTTP_TIMEOUT: int = 10
	# HTTP_RETRIES: int = 3

	# Logger
	LOGGER_LEVEL: str
	LOGGER_FORMAT: str

	LOGGER_DIR: Path
	LOGGER_ENABLE_FILE_LOGGING: bool
	LOGGER_ENABLE_CONSOLE_LOGGING: bool

	LOGGER_MAX_LOG_SIZE: int
	LOGGER_BACKUP_COUNT: int

	@computed_field
	@property
	def DATABASE_DSN(self) -> str:
		return f"postgresql://{self.DATABASE_USER}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"

	@computed_field
	@property
	def REDIS_DSN(self) -> str:
		if self.REDIS_USERNAME and self.REDIS_PASSWORD:
			# Redis 6+ с ACL
			return f"redis://{self.REDIS_USERNAME}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
		elif self.REDIS_PASSWORD:
			# Только пароль
			return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
		else:
			# Без аутентификации
			return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"

infrastructure_settings = InfrastructureSettings()
