import asyncpg
from asyncpg import Pool, Record
from asyncpg.pool import PoolConnectionProxy
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, AsyncIterator, List

from src.core.config import settings
from src.infrastructure.logger import get_logger

logger = get_logger("database")

@dataclass
class Transaction:
	"""Класс транзакции с удобным интерфейсом для запросов"""
	conn: PoolConnectionProxy

	async def fetch(self, query: str, *args: Any) -> List[Record]:
		return await self.conn.fetch(query, *args)

	async def fetchrow(self, query: str, *args: Any) -> Record | None:
		return await self.conn.fetchrow(query, *args)

	async def fetchval(self, query: str, *args: Any, column: int = 0) -> Any:
		return await self.conn.fetchval(query, *args, column=column)

	async def execute(self, query: str, *args: Any) -> str:
		return await self.conn.execute(query, *args)

	async def executemany(self, query: str, values: List[tuple]) -> None:
		await self.conn.executemany(query, values)

class Database:
	def __init__(self):
		self._pool: Pool | None = None

	@property
	def pool(self) -> Pool:
		if self._pool is None:
			raise RuntimeError("Database pool is not initialized")
		return self._pool

	async def connect(self) -> None:
		if self._pool is not None:
			return

		self._pool = await asyncpg.create_pool(dsn=str(settings.database.dsn))
		logger.info("🐘 Postgresql connected")

	async def close(self) -> None:
		if self._pool:
			await self._pool.close()
			self._pool = None
			logger.info("🐘 PostgreSQL disconnected")

	async def get_pool(self) -> Pool:
		await self.connect()
		return self.pool

	@asynccontextmanager
	async def transaction(self) -> AsyncIterator[Transaction]:
		"""Контекстный менеджер для транзакций с удобным интерфейсом"""
		async with self.pool.acquire() as conn:
			async with conn.transaction():
				yield Transaction(conn)

	async def fetch(self, query: str, *args: Any) -> List[Record]:
		"""Выполняет запрос и возвращает список записей."""
		async with self.pool.acquire() as conn:
			return await conn.fetch(query, *args)

	async def fetchrow(self, query: str, *args: Any) -> Record | None:
		"""Выполняет запрос и возвращает одну запись."""
		async with self.pool.acquire() as conn:
			return await conn.fetchrow(query, *args)

	async def fetchval(self, query: str, *args: Any, column: int = 0) -> Any:
		"""Выполняет запрос и возвращает значение."""
		async with self.pool.acquire() as conn:
			return await conn.fetchval(query, *args, column=column)

	async def execute(self, query: str, *args: Any) -> str:
		"""Выполняет запрос (INSERT/UPDATE/DELETE) и возвращает статус."""
		async with self.pool.acquire() as conn:
			return await conn.execute(query, *args)

	async def executemany(self, query: str, values: List[tuple]) -> None:
		"""Массовое выполнение запроса."""
		async with self.pool.acquire() as conn:
			await conn.executemany(query, values)

	@asynccontextmanager
	async def get_connection(self) -> AsyncIterator[PoolConnectionProxy]:
		"""Контекстный менеджер для FastAPI dependencies"""
		if self._pool is None:
			await self.connect()

		conn = await self.pool.acquire()

		try:
			yield conn
		finally:
			await self.pool.release(conn)

db = Database()
