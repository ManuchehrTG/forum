import json
from asyncpg import Pool
from typing import List
from uuid import UUID

from src.domain.sections.entities import Section
from src.domain.sections.exceptions import SectionNotFoundError
from src.domain.sections.repository import SectionRepository

class RawSQLSectionRepository(SectionRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def get_by_id(self, section_id: UUID) -> Section:
		async with self.pool.acquire() as connection:
			section_row = await connection.fetchrow("SELECT * FROM sections WHERE id = $1", section_id)
			if not section_row:
				raise SectionNotFoundError.by_id(section_id)

			section_message_type_rows = await connection.fetch("SELECT * FROM section_message_types WHERE section_id = $1", section_id)

			return Section.from_db_with_allowed_message_types(section_row, section_message_type_rows)

	async def get_by_code(self, section_code: str) -> Section:
		async with self.pool.acquire() as connection:
			section_row = await connection.fetchrow("SELECT * FROM sections WHERE code = $1", section_code)
			if not section_row:
				raise SectionNotFoundError.by_code(section_code)

			section_message_type_rows = await connection.fetch("SELECT * FROM section_message_types WHERE section_id = $1", section_row["id"])

			return Section.from_db_with_allowed_message_types(section_row, section_message_type_rows)

	async def get_list(self) -> List[Section]:
		async with self.pool.acquire() as connection:
			rows = await connection.fetch(
				"""
				SELECT 
					s.*,
					COALESCE(
						json_agg(smt) FILTER (WHERE smt.id IS NOT NULL),
						'[]'::json
					) AS section_message_types
				FROM sections s
				LEFT JOIN section_message_types smt ON s.id = smt.section_id
				GROUP BY s.id
				"""
			)

			return [Section.from_db_with_allowed_message_types(row, json.loads(row["section_message_types"])) for row in rows]

	async def save(self, section: Section) -> None:
		async with self.pool.acquire() as connection:
			async with connection.transaction():
				await connection.execute(
					"""
					INSERT INTO sections(id, code, openai_prompt, tech_version, allow_hide, created_at, updated_at)
					VALUES ($1, $2, $3, $4, $5, $6, $7)
					ON CONFLICT (id) DO UPDATE SET
						openai_prompt = EXCLUDED.openai_prompt,
						tech_version = EXCLUDED.tech_version,
						allow_hide = EXCLUDED.allow_hide,
						updated_at = EXCLUDED.updated_at
					""",
					section.id, section.code, section.openai_prompt, section.tech_version.value, section.allow_hide, section.created_at, section.updated_at
				)

				await connection.execute("DELETE FROM section_message_types WHERE section_id = $1", section.id)

				for amt in section.allowed_message_types:
					await connection.execute(
						"""
						INSERT INTO section_message_types (section_id, message_type, allow_comments)
						VALUES ($1, $2, $3)
						""",
						section.id, amt.message_type.value, amt.allow_comments
					)
