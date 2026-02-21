from fastapi import APIRouter, Depends
from typing import List

from . import schemas
from .dependencies import get_root_theme, get_theme, get_create_theme, get_retrieve_theme_sections
from src.api.v1.schemas import IdResponse
from src.api.v1.users.dependencies import get_current_user
from src.application.users.dtos import UserDTO
from src.application.themes.commands import CreateThemeCommand
from src.application.themes.dtos import ThemeDTO
from src.application.themes.queries import GetThemeSectionsQuery
from src.application.themes.use_cases.create import CreateTheme
from src.application.themes.use_cases.get_theme_sections import GetThemeSections

router = APIRouter(prefix="/themes", tags=["Themes"])

@router.post("", response_model=IdResponse, status_code=201, summary="Create theme", description="<b>Создать новую тему.</b>")
async def create_theme_endpoint(
	request: schemas.ThemeCreateRequest,
	user: UserDTO = Depends(get_current_user),
	create_theme: CreateTheme = Depends(get_create_theme)
):
	command = CreateThemeCommand(
		author_id=user.id,
		**request.model_dump()
	)
	theme_id = await create_theme.execute(command)
	return IdResponse(id=theme_id)

@router.get("/root", response_model=schemas.ThemeResponse, summary="Get root theme", description="<b>Получить корневую-главную тему.</b>")
async def get_root_theme_endpoint(
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_root_theme)
):
	return schemas.ThemeResponse.from_orm(theme)

@router.get("/{theme_id}", response_model=schemas.ThemeResponse, summary="Get theme", description="<b>Получить конкретную тему.</b>")
async def get_theme_endpoint(
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme)
):
	return schemas.ThemeResponse.from_orm(theme)

@router.get("/{theme_id}/sections", response_model=List[schemas.ThemeSectionResponse], summary="Get theme sections", description="<b>Получить доступные секции темы.</b>")
async def get_theme_sections_endpoint(
	user: UserDTO = Depends(get_current_user),
	theme: ThemeDTO = Depends(get_theme),
	get_theme_sections: GetThemeSections = Depends(get_retrieve_theme_sections)
):
	query = GetThemeSectionsQuery(theme_id=theme.id)
	theme_sections = await get_theme_sections.execute(query)
	return [schemas.ThemeSectionResponse.from_orm(ts) for ts in theme_sections]
