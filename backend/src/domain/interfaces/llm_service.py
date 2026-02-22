from typing import Protocol

from src.application.llm.commands import LLMCommand
from src.application.llm.dtos import LLMResultDTO

class LLMService(Protocol):
	async def generate(self, command: LLMCommand) -> LLMResultDTO:
		...
