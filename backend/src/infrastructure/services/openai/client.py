import httpx
from openai import AsyncOpenAI

from src.core.config import settings

openai_client = AsyncOpenAI(api_key=settings.openai.api_key, http_client=httpx.AsyncClient(proxy=settings.proxy.http))
