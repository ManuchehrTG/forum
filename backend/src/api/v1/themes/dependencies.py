from asyncpg import Pool
from fastapi import Depends
from uuid import UUID

from src.api.dependencies import get_db_pool
from src.api.v1.sections.dependencies import get_section_repository
from src.application.themes.dtos import ThemeDTO
from src.application.themes.queries import GetThemeQuery
from src.application.themes.use_cases.create import CreateTheme
from src.application.themes.use_cases.get import GetTheme
from src.application.themes.use_cases.get_root import GetRootTheme
from src.application.themes.use_cases.get_theme_sections import GetThemeSections
from src.domain.themes.repository import ThemeRepository
from src.domain.sections.repository import SectionRepository
from src.infrastructure.database.repositories.raw_sql.themes import RawSQLThemeRepository

async def get_theme_repository(
	pool: Pool = Depends(get_db_pool)
) -> ThemeRepository:
	return RawSQLThemeRepository(pool)


async def get_create_theme(
	theme_repo: ThemeRepository = Depends(get_theme_repository),
	section_repo: SectionRepository = Depends(get_section_repository)
) -> CreateTheme:
	return CreateTheme(theme_repo, section_repo)

async def get_retrieve_theme_sections(
	theme_repo: ThemeRepository = Depends(get_theme_repository),
) -> GetThemeSections:
	return GetThemeSections(theme_repo)

async def get_retrieve_theme(
	repository: ThemeRepository = Depends(get_theme_repository)
) -> GetTheme:
	return GetTheme(repository)

async def get_retrieve_root_theme(
	repository: ThemeRepository = Depends(get_theme_repository)
) -> GetRootTheme:
	return GetRootTheme(repository)


async def get_root_theme(
	get_root_theme: GetRootTheme = Depends(get_retrieve_root_theme)
) -> ThemeDTO:
	return await get_root_theme.execute()

async def get_theme(
	theme_id: UUID,
	get_theme: GetTheme = Depends(get_retrieve_theme)
) -> ThemeDTO:
	query = GetThemeQuery(theme_id=theme_id)
	return await get_theme.execute(query)
