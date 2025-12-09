from app.core.exceptions import NotFoundError
from app.domains.user.schemas.user import User
from ..repositories import ThemeRepository
from ..schemas import ThemeCreateRequest, Theme
from .theme_section import ThemeSectionService

class ThemeService:
	def __init__(self, theme_section_service: ThemeSectionService):
		self.theme_section_service = theme_section_service

	async def create_theme(self, data: ThemeCreateRequest, user: User) -> Theme:
		theme = await ThemeRepository.create_theme(data=data, author_id=user.id)
		await self.theme_section_service.create_theme_sections(theme_id=theme.id, tech_version=data.tech_version)

		return theme

	async def get_theme_by_id(self, theme_id: int) -> Theme:
		theme = await ThemeRepository.get_theme_by_id(theme_id=theme_id)
		if not theme:
			raise NotFoundError(entity="Theme", entity_id=theme_id)

		return theme
