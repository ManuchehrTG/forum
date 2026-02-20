from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool

from src.infrastructure.logger import get_logger

logger = get_logger("redis")

class RedisDB:
	def __init__(self) -> None:
		self._redis: Redis | None = None

	@property
	def redis(self) -> Redis:
		if self._redis is None:
			raise RuntimeError("Redis is not initialized")
		return self._redis

	async def connect(self, connection_url: str) -> None:
		try:
			pool = ConnectionPool.from_url(connection_url, decode_responses=True)
			self._redis = Redis(connection_pool=pool)
			await self._redis.ping() # pyright: ignore[reportGeneralTypeIssues]
			logger.info("⚡️ Redis connected")
		except Exception as e:
			logger.info("Redis connection failed")
			raise e

	async def close(self) -> None:
		if self._redis:
			await self._redis.aclose()
			self._redis = None
			logger.info("⚡️ Redis disconnected")

	def get_redis(self) -> Redis:
		return self.redis

redis = RedisDB()
