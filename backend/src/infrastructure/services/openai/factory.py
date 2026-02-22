from .client import openai_client
from .service import OpenAIService

def create_openai_service(model: str = "gpt-4"):
	"""Фабрика для создания openai service"""
	return OpenAIService(client=openai_client, model=model)
