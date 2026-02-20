import asyncio

from src.infrastructure.database import db
from src.infrastructure.database.repositories.raw_sql.users import RawSQLUserRepository
from src.infrastructure.database.repositories.raw_sql.themes import RawSQLThemeRepository
from src.infrastructure.database.repositories.raw_sql.sections import RawSQLSectionRepository
from src.infrastructure.database.seeds.users import seed_users
from src.infrastructure.database.seeds.sections import seed_sections
from src.infrastructure.database.seeds.themes import seed_themes

async def main():
	pool = await db.get_pool()

	user_repo = RawSQLUserRepository(pool)
	section_repo = RawSQLSectionRepository(pool)
	theme_repo = RawSQLThemeRepository(pool)

	await seed_users(user_repo)
	await seed_sections(section_repo)
	await seed_themes(theme_repo, section_repo)

	await db.close()

if __name__ == "__main__":
	asyncio.run(main())
