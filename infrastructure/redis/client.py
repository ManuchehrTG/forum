import os
from redis.asyncio.client import Redis
from redis.asyncio.connection import ConnectionPool
from redis.exceptions import RedisError, ConnectionError

from infrastructure.config import infrastructure_settings
from infrastructure.logger import get_logger

# REDIS_HOST = os.getenv("REDIS_HOST")
# REDIS_PORT = os.getenv("REDIS_PORT")
# REDIS_DB = os.getenv("REDIS_DB")

# REDIS_DSN = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"

logger = get_logger("redis")

pool = ConnectionPool.from_url(infrastructure_settings.REDIS_DSN)
redis = Redis(connection_pool=pool)

async def check_redis():
	try:
		await redis.ping()
		logger.info("⚡️ Redis connected")
	except Exception as e:
		logger.info("Redis connection failed")
		raise e
