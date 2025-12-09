from .factory import create_openai_service
from .services import OpenAIService

def get_openai_service() -> OpenAIService:
	return create_openai_service()
