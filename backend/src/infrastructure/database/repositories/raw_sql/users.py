import json
import uuid
from asyncpg import Pool

from src.domain.users.entities import User, LinkedAccount
from src.domain.users.exceptions import UserNotFoundError
from src.domain.users.value_objects import AuthProviderType
from src.domain.users.repository import UserRepository

class RawSQLUserRepository(UserRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def get_by_id(self, user_id: uuid.UUID) -> User:
		async with self.pool.acquire() as connection:
			user_row = await connection.fetchrow("SELECT * FROM users WHERE id = $1", user_id)
			if not user_row:
				raise UserNotFoundError.by_id(user_id)

			account_rows = await connection.fetch("SELECT * FROM linked_accounts WHERE user_id = $1", user_id)

			return User.from_db_with_accounts(user_row, account_rows)

	async def get_by_provider_user_id(self, provider: AuthProviderType, provider_user_id: str) -> User:
		async with self.pool.acquire() as connection:
			user_row = await connection.fetchrow(
				"""
				SELECT u.*
				FROM users u
				JOIN linked_accounts la
					ON u.id = la.user_id
				WHERE la.provider_user_id = $1 AND la.provider = $2
				""",
				provider_user_id, provider.value
			)
			if not user_row:
				raise UserNotFoundError.by_provider(provider.value, provider_user_id)

			account_rows = await connection.fetch("SELECT * FROM linked_accounts WHERE provider_user_id = $1", provider_user_id)

			return User.from_db_with_accounts(user_row, account_rows)

	async def add(self, user: User) -> None:
		async with self.pool.acquire() as connection:
			async with connection.transaction():
				await connection.execute(
					"""
					INSERT INTO users(id, first_name, last_name, username, email, phone, language_code, avatar_path, is_system, created_at, updated_at)
					VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
					""",
					user.id, user.first_name, user.last_name, user.username, user.email, user.phone, user.language_code, user.avatar_path,
					user.is_system, user.created_at, user.updated_at
				)

				for account in user.accounts:
					await connection.execute(
						"""
						INSERT INTO linked_accounts(user_id, provider, provider_user_id, extra, created_at, updated_at)
						VALUES ($1, $2, $3, $4, $5, $6)
						""",
						user.id, account.provider.value, account.provider_user_id, json.dumps(account.extra), account.created_at, account.updated_at
					)

	async def update(self, user: User) -> None:
		async with self.pool.acquire() as connection:
			await connection.execute(
				"""
				UPDATE users SET
					first_name=$1,
					last_name=$2,
					username=$3,
					updated_at=$4
				WHERE id=$5
				""",
				user.first_name, user.last_name, user.username, user.updated_at, user.id
			)

	async def set_avatar(self, user_id: uuid.UUID, avatar_path: str) -> None:
		async with self.pool.acquire() as connection:
			await connection.execute(
				"""
				UPDATE users SET
					avatar_path=$1
				WHERE id=$2
				""",
				avatar_path, user_id
			)
