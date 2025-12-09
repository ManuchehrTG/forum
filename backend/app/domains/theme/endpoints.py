from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.domains.auth.dependencies import get_current_user
from app.domains.user.schemas import User
from .adapters import theme_to_response
from .dependencies import get_theme_service, get_theme_section_service, get_theme
from .schemas.theme import Theme, ThemeCreateRequest, ThemeResponse
from .services import ThemeService, ThemeSectionService

router = APIRouter(prefix="/api/v1/themes", tags=["Themes"])

@router.post("", response_model=ThemeResponse)
async def create_theme_endpoint(
	data: ThemeCreateRequest,
	user: User = Depends(get_current_user),
	theme_service: ThemeService = Depends(get_theme_service)
):
	theme = await theme_service.create_theme(data=data, user=user)
	return theme_to_response(theme=theme)
	# except Exception as e:
	# 	raise e # Конфликт 409

@router.get("/{theme_id}", response_model=ThemeResponse)
async def get_theme_endpoint(
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme)
):
	return theme_to_response(theme=theme)

@router.get("/{theme_id}/sections", response_model=List[str])
async def get_theme_section_codes_endpoint(
	user: User = Depends(get_current_user),
	theme: Theme = Depends(get_theme),
	theme_section_service: ThemeSectionService = Depends(get_theme_section_service)
):
	return await theme_section_service.get_theme_section_codes(theme_id=theme.id)
