from asyncpg import Pool
from asyncpg.pool import PoolConnectionProxy
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator, AsyncIterator

from src.domain.users.exceptions import InvalidTokenError, TokenExpiredError
from src.infrastructure.auth.jwt import JWTManager
from src.infrastructure.database import db, get_session

security = HTTPBearer()

async def get_token_payload(
	credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
	"""Базовый dependency для получения payload из токена"""
	try:
		return JWTManager.verify_token(credentials.credentials)
	except (InvalidTokenError, TokenExpiredError) as e:
		raise HTTPException(
			status_code=401,
			detail={
				"code": e.error_code,
				"message": e.message
			},
			headers={"WWW-Authenticate": "Bearer"},
		)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
	async for session in get_session():
		yield session

async def get_db_connection() -> AsyncIterator[PoolConnectionProxy]:
	async with db.get_connection() as conn:
		yield conn

async def get_db_pool() -> Pool:
	"""Зависимость для получения пула соединений"""
	if db._pool is None:
		await db.connect()
	return db.pool
