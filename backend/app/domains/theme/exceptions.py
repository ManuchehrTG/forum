from app.core.exceptions import AppError

class ThemeSectionDisabledError(AppError):
	"""Секция отключена администратором для данной темы"""
	def __init__(self, theme_id: int, section_code: str, available_sections: list[str] = None):
		super().__init__(
			message=f"Section `{section_code}` is disabled for theme_id={theme_id}",
			code="theme_section_disabled",
			status_code=403,
			theme_id=theme_id,
			section_code=section_code,
			available_sections=available_sections
		)
