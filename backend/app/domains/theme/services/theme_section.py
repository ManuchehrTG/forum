from typing import List

from app.domains.section.repositories import SectionRepository
from app.domains.section.schemas import Section
from ..exceptions import ThemeSectionDisabledError
from ..repositories import ThemeSectionRepository
from ..schemas import ThemeTechVersionType

class ThemeSectionService:
	async def create_theme_sections(self, theme_id: int, tech_version: ThemeTechVersionType) -> None:
		tech_versions_map = {
			ThemeTechVersionType.MINIMUM: ["minimum"],
			ThemeTechVersionType.FULL: ["minimum", "full"],
		}
		tech_versions = tech_versions_map[tech_version]

		sections = await SectionRepository.get_sections_by_tech_version(tech_versions=tech_versions)
		await ThemeSectionRepository.create_theme_sections(theme_id=theme_id, sections=sections)

	async def get_theme_section_codes(self, theme_id: int) -> List[str]:
		return await ThemeSectionRepository.get_theme_section_codes(theme_id=theme_id)

	async def _validate_theme_section_access(self, theme_id: int, section_code: str) -> None:
		available_sections = await self.get_theme_section_codes(theme_id=theme_id)

		if section_code not in available_sections:
			raise ThemeSectionDisabledError(theme_id=theme_id, section_code=section_code, available_sections=available_sections)
