from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.themes.commands import CreateThemeCommand
from src.domain.themes.entities import Theme
from src.domain.themes.exceptions import ThemeNotFoundError
from src.domain.themes.repository import ThemeRepository
from src.domain.sections.repository import SectionRepository
from src.domain.sections.value_objects import TechVersionType

class CreateTheme:
	def __init__(self, theme_repo: ThemeRepository, section_repo: SectionRepository):
		self.theme_repo = theme_repo
		self.section_repo = section_repo

	@handle_domain_errors
	async def execute(self, command: CreateThemeCommand) -> UUID:
		parent_id = None
		if command.parent_id:
			try:
				await self.theme_repo.get_by_id(command.parent_id)
				parent_id = command.parent_id
			except ThemeNotFoundError:
				parent_id = None

		tech_version_enum = TechVersionType(command.tech_version)

		theme = Theme(
			parent_id=parent_id,
			author_id=command.author_id,
			title=command.title,
			is_group=command.is_group,
		)

		sections = await self.section_repo.get_list()

		for section in sections:
			is_visible = tech_version_enum.can_include(section.tech_version)
			theme.add_section(section.id, section.code, is_visible=is_visible)

		await self.theme_repo.save(theme)

		return theme.id
