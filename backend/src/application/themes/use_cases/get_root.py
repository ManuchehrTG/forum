from src.application.decorators import handle_domain_errors
from src.application.themes.dtos import ThemeDTO
from src.core.config import settings
from src.domain.themes.entities.theme import Theme
from src.domain.themes.repository import ThemeRepository

class GetRootTheme:
	def __init__(self, theme_repo: ThemeRepository):
		self.theme_repo = theme_repo

	@handle_domain_errors
	async def execute(self) -> ThemeDTO:
		theme = await self.theme_repo.get_root(settings.system_user_id)

		return self._to_dto(theme)

	def _to_dto(self, theme: Theme) -> ThemeDTO:
		return ThemeDTO(
			id=theme.id,
			parent_id=theme.parent_id,
			author_id=theme.author_id,
			title=theme.title,
			is_group=theme.is_group,
			created_at=theme.created_at,
			updated_at=theme.updated_at
		)
