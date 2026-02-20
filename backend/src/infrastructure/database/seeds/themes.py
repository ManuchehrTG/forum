from src.core.config import settings
from src.domain.sections.repository import SectionRepository
from src.domain.sections.value_objects import TechVersionType
from src.domain.themes.entities import Theme
from src.domain.themes.exceptions import ThemeNotFoundError
from src.domain.themes.repository import ThemeRepository

THEMES = [
	{
		"author_id": settings.system_user_id,
		"title": "Проект всего",
		"tech_version": TechVersionType.FULL
	},
]

async def seed_themes(theme_repo: ThemeRepository, section_repo: SectionRepository):
	for item in THEMES:
		try:
			await theme_repo.get_by_title(item["title"])
			continue
		except ThemeNotFoundError:
			theme = Theme(author_id=item["author_id"], title=item["title"])
			sections = await section_repo.get_list()

			for section in sections:
				is_visible = item["tech_version"].can_include(section.tech_version)
				theme.add_section(section.id, section.code, is_visible=is_visible)

			await theme_repo.save(theme)
