from infrastructure.database import db
from ..schemas import LinkedAccountCreateData, LinkedAccount

class LinkedAccountRepository:
	@staticmethod
	async def create_linked_account(data: LinkedAccountCreateData) -> LinkedAccount:
		record = await db.fetchrow(
			"""
			INSERT INTO linked_accounts (user_id, provider, provider_user_id, extra)
			VALUES ($1, $2, $3, $4)
			RETURNING *
			""",
			data.user_id, data.provider, data.provider_user_id, data.extra_json
		)
		return LinkedAccount(**record)
