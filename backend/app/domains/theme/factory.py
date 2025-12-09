from app.domains.user.services import UserService, LinkedAccountService
from .services import ThemeService, ThemeSectionService

def create_theme_service() -> ThemeService:
	return ThemeService(
		theme_section_service=ThemeSectionService()
	)

def create_theme_section_service() -> ThemeSectionService:
	return ThemeSectionService()
