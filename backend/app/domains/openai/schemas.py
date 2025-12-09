from pydantic import BaseModel, Field, field_validator

class OpenAIGenerateTextRequest(BaseModel):
	text: str = Field(..., min_length=3, description="Текст для обработки с OpenAI")

	@field_validator("text")
	@classmethod
	def validate_text_not_empty(cls, v: str) -> str:
		if not v or not v.strip():
			raise ValueError("Text cannot be empty")
		return v.strip()

class OpenAIGenerateText(BaseModel):
	original_text: str = Field(..., description="Текст оригинал")
	openai_text: str | None = Field(None, description="Текст сгенерированный с помощью OpenAI")

class OpenAIGenerateTextResponse(OpenAIGenerateText):
	pass
