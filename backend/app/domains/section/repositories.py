from typing import List

from infrastructure.database import db
from .schemas import Section

class SectionRepository:
	@staticmethod
	async def get_sections_by_tech_version(tech_versions: List[str]) -> List[Section]:
		print("tech_versions:", tech_versions)
		records = await db.fetch("SELECT * FROM sections WHERE tech_version = ANY($1)", tech_versions)
		return [Section(**record) for record in records]

	@staticmethod
	async def get_section_by_code(section_code: str) -> Section | None:
		record = await db.fetchrow("SELECT * FROM sections WHERE code = $1", section_code)
		if record:
			return Section(**record)
