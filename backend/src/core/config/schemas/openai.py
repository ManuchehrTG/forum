from pydantic_settings import BaseSettings

class OpenaiSettings(BaseSettings):
	api_key: str

	class Config:
		env_prefix = "OPENAI_"
		case_sensitive = False
