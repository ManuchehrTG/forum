from uuid import UUID

from infrastructure.database import db
from ..schemas import Theme, ThemeCreateRequest

class ThemeRepository:
	@staticmethod
	async def create_theme(data: ThemeCreateRequest, author_id: UUID):
		record = await db.fetchrow(
			"""
			INSERT INTO themes (parent_id, author_id, title)
			VALUES ($1, $2, $3)
			RETURNING *
			""",
			data.parent_id, author_id, data.title
		)
		return Theme(**record)

	@staticmethod
	async def get_theme_by_id(theme_id: int):
		record = await db.fetchrow("SELECT * FROM themes WHERE id = $1", theme_id)
		if record:
			return Theme(**record)

