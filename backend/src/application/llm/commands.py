from pydantic import BaseModel

class LLMCommand(BaseModel):
	prompt: str
	input_text: str
	temperature: float = 0.7
