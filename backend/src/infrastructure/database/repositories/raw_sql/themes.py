from asyncpg import Pool
from uuid import UUID

from src.domain.themes.entities import Theme
from src.domain.themes.exceptions import ThemeNotFoundError
from src.domain.themes.repository import ThemeRepository

class RawSQLThemeRepository(ThemeRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def get_by_id(self, theme_id: UUID) -> Theme:
		async with self.pool.acquire() as connection:
			theme_row = await connection.fetchrow("SELECT * FROM themes WHERE id = $1", theme_id)
			if not theme_row:
				raise ThemeNotFoundError.by_id(theme_id)

			section_rows = await connection.fetch(
				"""
				SELECT
					ts.*,
					s.code AS section_code
				FROM theme_sections ts
				JOIN sections s ON ts.section_id = s.id
				WHERE ts.theme_id = $1
				""",
				theme_id
			)

			return Theme.from_db_with_sections(theme_row, section_rows)

	async def get_by_title(self, title: str) -> Theme:
		async with self.pool.acquire() as connection:
			theme_row = await connection.fetchrow("SELECT * FROM themes WHERE title = $1", title)
			if not theme_row:
				raise ThemeNotFoundError.by_title(title)

			section_rows = await connection.fetch(
				"""
				SELECT
					ts.*,
					s.code AS section_code
				FROM theme_sections ts
				JOIN sections s ON ts.section_id = s.id
				WHERE ts.theme_id = $1
				""",
				theme_row["id"]
			)

			return Theme.from_db_with_sections(theme_row, section_rows)

	async def get_root(self, system_user_id: UUID) -> Theme:
		async with self.pool.acquire() as connection:
			theme_row = await connection.fetchrow("SELECT * FROM themes WHERE author_id = $1", system_user_id)
			section_rows = await connection.fetch(
				"""
				SELECT
					ts.*,
					s.code AS section_code
				FROM theme_sections ts
				JOIN sections s ON ts.section_id = s.id
				WHERE ts.theme_id = $1
				""",
				theme_row["id"]
			)
			return Theme.from_db_with_sections(theme_row, section_rows)

	async def save(self, theme: Theme) -> None:
		async with self.pool.acquire() as connection:
			async with connection.transaction():
				await connection.execute(
					"""
					INSERT INTO themes (id, parent_id, author_id, title, is_group, created_at, updated_at)
					VALUES ($1, $2, $3, $4, $5, $6, $7)
					ON CONFLICT (id) DO UPDATE SET
						parent_id = EXCLUDED.parent_id,
						author_id = EXCLUDED.author_id,
						title = EXCLUDED.title,
						is_group = EXCLUDED.is_group,
						updated_at = EXCLUDED.updated_at
					""",
					theme.id, theme.parent_id, theme.author_id, theme.title, theme.is_group, theme.created_at, theme.updated_at
				)

				await connection.execute("DELETE FROM theme_sections WHERE theme_id = $1", theme.id)

				for ts in theme.sections:
					await connection.execute(
						"""
						INSERT INTO theme_sections (theme_id, section_id, is_visible)
						VALUES ($1, $2, $3)
						""",
						theme.id, ts.section_id, ts.is_visible
					)
