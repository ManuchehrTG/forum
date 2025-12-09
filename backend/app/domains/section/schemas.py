from pydantic import BaseModel, Field

class Section(BaseModel):
	code: str = Field(..., description="Уникальный ключ раздела")
	is_openai_enabled: bool = Field(..., description="Включен ли openai")
	openai_prompt: str | None = Field(None, description="Промпт для openai")
	allow_hide: bool = Field(..., description="Можно ли скрывать")
