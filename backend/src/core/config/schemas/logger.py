from pathlib import Path
from pydantic_settings import BaseSettings

class LoggerSettings(BaseSettings):
	level: str
	format: str

	dir: Path
	enable_file_logging: bool
	enable_console_logging: bool

	max_log_size: int
	backup_count: int

	class Config:
		env_prefix = "LOGGER_"
		case_sensitive = False
