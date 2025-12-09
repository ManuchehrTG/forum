from fastapi import Depends, HTTPException

from app.domains.section.dependencies import get_section
from app.domains.section.schemas import Section
from .factory import create_theme_service, create_theme_section_service
from .schemas import Theme
from .services import ThemeService, ThemeSectionService

def get_theme_service() -> ThemeService:
	return create_theme_service()

def get_theme_section_service() -> ThemeSectionService:
	return create_theme_section_service()

async def get_theme(
	theme_id: int,
	theme_service: ThemeService = Depends(get_theme_service)
) -> Theme:
	return await theme_service.get_theme_by_id(theme_id=theme_id)

async def get_theme_section(
	theme: Theme = Depends(get_theme),
	section: Section = Depends(get_section),
	theme_section_service: ThemeSectionService = Depends(get_theme_section_service)
) -> Section:
	await theme_section_service._validate_theme_section_access(theme_id=theme.id, section_code=section.code)
	return section
