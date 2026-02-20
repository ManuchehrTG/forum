from uuid import UUID

from src.shared.exceptions import NotFoundError

class ThemeNotFoundError(NotFoundError):
	"""Тема не найдена"""
	error_code = "theme_not_found"

	def __init__(self, theme_id: str | UUID, search_type: str, **kwargs):
		super().__init__(entity="Theme", entity_id=str(theme_id), search_type=search_type, **kwargs)

	@classmethod
	def by_id(cls, theme_id: str | UUID, **kwargs) -> "ThemeNotFoundError":
		return cls(theme_id=theme_id, search_type="id", **kwargs)

	@classmethod
	def by_title(cls, theme_title: str, **kwargs) -> "ThemeNotFoundError":
		return cls(theme_id=theme_title, search_type="title", **kwargs)

class ThemeSectionNotFoundError(NotFoundError):
	"""Секция темы не найдена"""
	def __init__(self, theme_id: str | UUID, section_id: str | UUID, **kwargs):
		entity_id = f"<Theme:{theme_id}>, <Section:{section_id}>"
		super().__init__(entity="Theme and Section", entity_id=entity_id, **kwargs)
