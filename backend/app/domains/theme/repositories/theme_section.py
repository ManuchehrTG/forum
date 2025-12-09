from typing import List

from app.domains.section.schemas import Section
from infrastructure.database import db

class ThemeSectionRepository:
	@staticmethod
	async def create_theme_sections(theme_id: int, sections: List[Section]):
		values = [(theme_id, section.code) for section in sections]

		await db.executemany(
			"""
			INSERT INTO theme_sections (theme_id, section_code)
			VALUES ($1, $2)
			ON CONFLICT (theme_id, section_code) DO NOTHING
			""",
			values
		)

	@staticmethod
	async def get_theme_section_codes(theme_id: int) -> List[str]:
		records = await db.fetch(
			"""
			SELECT section_code
			FROM theme_sections
			WHERE theme_id = $1 AND is_visible = TRUE
			""",
			theme_id
		)
		return [record["section_code"] for record in records]

	@staticmethod
	async def get_theme_section(theme_id: int, section_code: str) -> Section | None:
		record = await db.fetchrow(
			"""
			SELECT s.*
			FROM sections s
			LEFT JOIN theme_sections ts ON ts.section_code = s.code
			WHERE ts.theme_id = $1 AND ts.section_code = $2 AND ts.is_visible = TRUE
			""",
			theme_id, section_code
		)
		if record:
			return Section(**record)
