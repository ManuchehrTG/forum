from asyncpg import Pool
from fastapi import Depends, HTTPException

from src.application.users.queries import GetUserQuery
from src.application.users.use_cases.get import GetUser
from src.infrastructure.auth.jwt import JWTManager
from src.api.dependencies import get_token_payload, get_db_pool
from src.application.users.dtos import UserDTO
from src.application.users.use_cases.update_avatar import UpdateUserAvatar
from src.domain.users.avatar_downloader import AvatarDownloader
from src.domain.users.exceptions import InvalidTokenError
from src.domain.users.repository import UserRepository
from src.infrastructure.avatar_downloaders import create_avatar_downloader
from src.infrastructure.database.repositories.raw_sql.users import RawSQLUserRepository

async def get_user_repository(
	pool: Pool = Depends(get_db_pool)
) -> UserRepository:
	return RawSQLUserRepository(pool)

async def get_avatar_downloader() -> AvatarDownloader:
	return create_avatar_downloader()

async def get_retrieve_user(
	user_repo: UserRepository = Depends(get_user_repository),
) -> GetUser:
	return GetUser(user_repo)

async def get_update_user_avatar(
	user_repo: UserRepository = Depends(get_user_repository),
	downloader: AvatarDownloader = Depends(get_avatar_downloader)
) -> UpdateUserAvatar:
	return UpdateUserAvatar(user_repo, downloader)

async def get_current_user(
	payload: dict = Depends(get_token_payload),
	get_user: GetUser = Depends(get_retrieve_user)
) -> UserDTO:
		"""
		Получить текущего аутентифицированного пользователя.

		Проверки:
		1. Тип токена (должен быть access)
		2. Наличие user_id и provider в payload
		"""

		token_type = payload.get("type")
		if token_type != "access":
			# тут лучше вызвать готовый вариант из src/shared/exceptions/api.py UnauthorizedError - статус=401 или из src/domain/users/exceptions.py InvalidTokenError - без статус кода
			raise HTTPException(
				status_code=401,
				detail={
					"code": "invalid_token_type",
					"message": f"Expected access token, got {token_type}"
				},
				headers={"WWW-Authenticate": "Bearer"},
			)

		try:
			provider_user_id = JWTManager.extract_user_id_from_payload(payload)
			provider = JWTManager.extract_provider_from_payload(payload) # "telegram"
		except InvalidTokenError as e:
			raise HTTPException(
				status_code=401,
				detail={
					"code": e.error_code,
					"message": e.message
				},
				headers={"WWW-Authenticate": "Bearer"},
			)

		query = GetUserQuery.by_provider_id(provider=provider, provider_user_id=provider_user_id)
		return await get_user.execute(query=query)
