from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
	### Без BACKEND_
	PROJECT_NAME: str
	LANGUAGES: List[str] = Field(default_factory=list)
	DEFAULT_LANGUAGE: str

	DOWNLOAD_DIR: str
	STORAGE_DIR: str

	### С BACKEND_
	SECRET_KEY: str = Field(alias="BACKEND_SECRET_KEY")

	DOMAIN: str = Field(alias="BACKEND_DOMAIN")
	HOST: str = Field(alias="BACKEND_HOST")
	PORT: int = Field(alias="BACKEND_PORT")

	DEBUG: bool = Field(alias="BACKEND_DEBUG")
	ALLOWED_ORIGINS: List[str] = Field(default_factory=list, alias="BACKEND_ALLOWED_ORIGINS")

	ALGORITHM: str = Field(alias="BACKEND_ALGORITHM")
	JWT_TOKEN_EXPIRE_SECONDS: int = Field(alias="BACKEND_JWT_TOKEN_EXPIRE_SECONDS")
	JWT_TOKEN_GRACE_PERIOD_FOR_RENEWAL_SECONDS: int = Field(alias="BACKEND_JWT_TOKEN_GRACE_PERIOD_FOR_RENEWAL_SECONDS")
	AUTH_DATE_EXPIRE_SECONDS: int = Field(alias="BACKEND_AUTH_DATE_EXPIRE_SECONDS")

	### Без BACKEND_
	TELEGRAM_BOT_TOKEN: str


	OPENAI_API_KEY: str

	PROXY_HTTP: str
	PROXY_SOCKS5: str

	class Config:
		env_file = ".env"
		env_file_encoding = "utf-8"

settings = Settings()
