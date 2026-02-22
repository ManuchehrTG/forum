from openai import BaseModel

class LLMResultDTO(BaseModel):
	input_text: str
	output_text: str | None
