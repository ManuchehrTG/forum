import asyncio
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.domains.auth import endpoints as auth
from app.domains.user import endpoints as user
from app.domains.theme import endpoints as theme
from app.domains.message import endpoints as message
from app.core.config import settings, database_config
from app.core.exceptions import setup_exception_handlers
from infrastructure.database import db
from infrastructure.logger import logger

async def create_app() -> FastAPI:
	logger.info("🟢 Starting application...")
	await db.connect(connection_url=str(database_config.DSN))

	@asynccontextmanager
	async def lifespan(app: FastAPI):
		try:
			yield
		except Exception as e:
			logger.error(f"⚠️ Startup failed: {e}", exc_info=True)
			raise
		finally:
			logger.info("🔴 Shutting down...")
			try:
				await db.close()
			except Exception as e:
				logger.error(f"Error during shutdown: {e}", exc_info=True)

	app = FastAPI(
		title=settings.PROJECT_NAME,
		version="1.0.0",
		lifespan=lifespan,
		docs_url="/api/docs" if settings.DEBUG else None,
		swagger_ui_parameters={"operationsSorter": "method"}
	)

	setup_exception_handlers(app)

	app.add_middleware(
		CORSMiddleware,
		allow_origins=settings.ALLOWED_ORIGINS,
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
		expose_headers=["New-Access-Token"]
	)

	app.include_router(auth.router)
	app.include_router(user.router)
	app.include_router(theme.router)
	app.include_router(message.router)
	# app.include_router(attachment.router)

	app.mount(
		"/static/avatars",
		StaticFiles(directory=Path(settings.STORAGE_DIR) / "avatars"),
		name="avatars"
	)

	app.mount(
		"/static/messages",
		StaticFiles(directory=Path(settings.STORAGE_DIR) / "messages"),
		name="messages"
	)

	return app

async def main() -> None:
	app = await create_app()

	config = uvicorn.Config(app=app, host=settings.HOST, port=settings.PORT, log_level="info")
	server = uvicorn.Server(config)

	await server.serve()

if __name__ == "__main__":
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		logger.info("🔴 Server stopped gracefully")
