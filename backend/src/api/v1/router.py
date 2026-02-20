from fastapi import APIRouter

from .auth.endpoints import router as auth_router
from .users.endpoints import router as users_router
from .themes.endpoints import router as themes_router
from .messages.endpoints import router as messages_router
from .media_files.endpoints import router as media_files_router

router = APIRouter(prefix="/v1")

# Подключаем все роутеры
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(themes_router)
router.include_router(messages_router)
router.include_router(media_files_router)
