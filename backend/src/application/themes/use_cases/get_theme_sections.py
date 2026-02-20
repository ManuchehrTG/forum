from typing import List

from src.application.decorators import handle_domain_errors
from src.application.themes.dtos import ThemeSectionDTO
from src.application.themes.queries import GetThemeSectionsQuery
from src.domain.themes.repository import ThemeRepository

class GetThemeSections:
	def __init__(self, theme_repo: ThemeRepository):
		self.theme_repo = theme_repo

	@handle_domain_errors
	async def execute(self, query: GetThemeSectionsQuery) -> List[ThemeSectionDTO]:
		theme = await self.theme_repo.get_by_id(query.theme_id)
		return [ThemeSectionDTO(section_id=ts.section_id, section_code=ts.section_code) for ts in theme.sections]
