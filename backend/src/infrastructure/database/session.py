from sqlalchemy.ext.asyncio import AsyncSession, AsyncConnection, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool, NullPool
from typing import AsyncGenerator

from src.core.config import settings

# Выбор пула в зависимости от окружения
def get_pool_class():
	"""Выбор пула соединений"""
	if settings.environment == "testing":
		return NullPool  # Для тестов
	else:
		return AsyncAdaptedQueuePool  # Для разработки и продакшена

# Асинхронный engine для PostgreSQL
engine = create_async_engine(
	str(settings.database.async_dsn),
	echo=settings.debug,
	echo_pool=settings.debug,
	poolclass=get_pool_class(),
	pool_pre_ping=True,
	future=True,
)

# Фабрика сессий
AsyncSessionLocal = async_sessionmaker(
	bind=engine,
	class_=AsyncSession,
	expire_on_commit=False,
	autoflush=True,
	autocommit=False,
)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
	"""Dependency БЕЗ автоматического коммита"""
	async with AsyncSessionLocal() as session:
		try:
			yield session
		finally:
			await session.close()

async def get_connection() -> AsyncGenerator[AsyncConnection, None]:
	"""Raw SQL connection"""
	async with engine.connect() as conn:
		try:
			yield conn
		finally:
			await conn.close()
