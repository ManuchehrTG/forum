from pydantic_settings import BaseSettings

class TelegramBotSettings(BaseSettings):
	token: str

	class Config:
		env_prefix = "TELEGRAM_BOT_"
		case_sensitive = False
