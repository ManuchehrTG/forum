# pyright: reportCallIssue=false

from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Literal
from uuid import UUID

from .schemas import AppSettings, DatabaseSettings, JWTSettings, LoggerSettings, OpenaiSettings, ProxySettings, RedisSettings, StorageSettings, TelegramBotSettings

class Settings(BaseSettings):
	environment: Literal["local", "staging", "production"]

	debug: bool
	allowed_origins: List[str] = Field(default_factory=list)
	allowed_hosts: List[str] = Field(default_factory=list)

	domain: str = Field(validation_alias="BACKEND_DOMAIN")
	host: str = Field(validation_alias="BACKEND_HOST")
	port: int = Field(validation_alias="BACKEND_PORT")

	system_user_id: UUID = Field(default=UUID("99999999-9999-9999-9999-999999999999"))

	app: AppSettings = AppSettings()
	database: DatabaseSettings = DatabaseSettings()
	jwt: JWTSettings = JWTSettings()
	logger: LoggerSettings = LoggerSettings()
	openai: OpenaiSettings = OpenaiSettings()
	proxy: ProxySettings = ProxySettings()
	redis: RedisSettings = RedisSettings()
	storage: StorageSettings = StorageSettings()
	telegram_bot: TelegramBotSettings = TelegramBotSettings()

	class Config:
		env_file = [".env"]
		env_file_encoding = "utf-8"

settings = Settings()
