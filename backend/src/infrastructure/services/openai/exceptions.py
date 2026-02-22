from src.shared.exceptions.infrastructure import ExternalServiceError

class OpenAIServiceError(ExternalServiceError):
	def __init__(self, service: str, original_error: Exception | None = None, **kwargs):
		super().__init__(service, original_error, **kwargs)
