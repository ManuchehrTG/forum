import httpx
from openai import AsyncOpenAI

from app.core.config import settings

class OpenAIClient:
	def __init__(self):
		self.client = AsyncOpenAI(
			api_key=settings.OPENAI_API_KEY,
			http_client=httpx.AsyncClient(verify=False, proxy=settings.PROXY_HTTP)
		)
