import asyncio
import os
import yaml
from pathlib import Path

from infrastructure.config import infrastructure_settings
from infrastructure.database import db
from infrastructure.logger import get_logger

# DB_NAME = os.getenv("DATABASE_NAME")
# DB_USER = os.getenv("DATABASE_USER")
# DB_PASSWORD = os.getenv("DATABASE_PASSWORD")
# DB_HOST = os.getenv("DATABASE_HOST")
# DB_PORT = os.getenv("DATABASE_PORT")

# DATABASE_DSN = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

logger = get_logger("database")

async def main():
	await db.connect(connection_url=infrastructure_settings.DATABASE_DSN)

	schema_path = Path(__file__).parent / "init_scripts/01_schema.sql"
	if schema_path.exists():
		schema_sql = schema_path.read_text(encoding="utf-8")
		await db.execute(schema_sql)

	sql_path = Path(__file__).parent / "init_scripts/02_insert_section.sql"
	yaml_path = Path(__file__).parent / "seed_data/sections.yaml"
	if sql_path.exists() and yaml_path.exists():
		with open(yaml_path, "r", encoding="utf-8") as f:
			data = yaml.safe_load(f)

		query = sql_path.read_text()

		values = [(section["code"], section.get("openai_prompt", None), section["allow_hide"], section.get("tech_version", None)) for section in data]
		await db.executemany(query, values)

	sql_path = Path(__file__).parent / "init_scripts/03_insert_theme.sql"
	if sql_path.exists():
		query = sql_path.read_text()
		await db.execute(query)

	sql_path = Path(__file__).parent / "init_scripts/04_insert_theme_sections.sql"
	yaml_path = Path(__file__).parent / "seed_data/sections.yaml"
	if sql_path.exists() and yaml_path.exists():
		with open(yaml_path, "r", encoding="utf-8") as f:
			data = yaml.safe_load(f)

		query = sql_path.read_text()

		values = [(1, section["code"]) for section in data]
		await db.executemany(query, values)

	await db.close()

	logger.info("Database initialized ✅")

if __name__ == "__main__":
	asyncio.run(main())
