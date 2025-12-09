from uuid import UUID

from app.domains.auth.schemas import AuthProviderType
from infrastructure.database import db
from ..schemas import UserCreateData, User

class UserRepository:
	@staticmethod
	async def create_user(data: UserCreateData) -> User:
		record = await db.fetchrow(
			"""
			INSERT INTO users (first_name, username, email, phone_number, language_code, avatar_url)
			VALUES ($1, $2, $3, $4, $5, $6)
			RETURNING *
			""",
			data.first_name,
			data.username,
			data.email,
			data.phone_number,
			data.language_code,
			data.avatar_url
		)
		return User(**record)

	@staticmethod
	async def get_user_by_id(user_id: UUID) -> User | None:
		record = await db.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
		if record:
			return User(**record)

	@staticmethod
	async def get_user_by_provider_user_id(provider_user_id: str, provider: AuthProviderType) -> User | None:
		record = await db.fetchrow(
			"""
			SELECT u.*
			FROM users u
			JOIN linked_accounts ula
				ON u.id = ula.user_id
			WHERE ula.provider_user_id = $1 AND ula.provider = $2
			""",
			provider_user_id, provider
		)
		if record:
			return User(**record)
