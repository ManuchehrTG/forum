import logging
import logging.config

from src.core.config import settings
from .config import LOGGING_CONFIG
from .utils import get_logger, log_execution_time, LoggerMixin

class LoggerSetup:
	def __init__(self):
		self.config = settings.logger
		self._initialized = False

	def setup_logging(self) -> None:
		"""Инициализация системы логирования"""
		if self._initialized:
			return

		# Создаем директорию для логов
		if self.config.enable_file_logging:
			self.config.dir.mkdir(parents=True, exist_ok=True)

		# Обновляем конфигурацию на основе настроек
		self._update_logging_config()

		# Применяем конфигурацию
		logging.config.dictConfig(LOGGING_CONFIG)
		self._initialized = True

		# Логируем успешную инициализацию
		logger = logging.getLogger("infrastructure.logger")
		logger.info("🚀 Logger initialized successfully")

	def _update_logging_config(self) -> None:
		# Обновляем уровни логирования
		LOGGING_CONFIG["root"]["level"] = self.config.level

		# Настраиваем обработчики
		handlers = []

		if self.config.enable_console_logging:
			handlers.append("console")
			LOGGING_CONFIG["handlers"]["console"]["level"] = self.config.level

		if self.config.enable_file_logging:
			log_file = self.config.dir / "app.log"
			LOGGING_CONFIG["handlers"]["file"]["filename"] = str(log_file)
			LOGGING_CONFIG["handlers"]["file"]["maxBytes"] = self.config.max_log_size * 1024 * 1024
			LOGGING_CONFIG["handlers"]["file"]["backupCount"] = self.config.backup_count
			LOGGING_CONFIG["handlers"]["file"]["level"] = self.config.level
			handlers.append("file")

		# Обновляем обработчик для логгера
		LOGGING_CONFIG["root"]["handlers"] = handlers

# Глобальная инициализация
logger_setup = LoggerSetup()
logger_setup.setup_logging()

# Экспорт основного логгера
logger = logging.getLogger()

__all__ = ["logger", "get_logger", "log_execution_time", "LoggerMixin"]
