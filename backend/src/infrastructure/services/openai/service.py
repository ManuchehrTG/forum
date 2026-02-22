from openai import AsyncOpenAI

from src.application.llm.commands import LLMCommand
from src.application.llm.dtos import LLMResultDTO

from .exceptions import OpenAIServiceError

class OpenAIService:
	"""Сервис для работы с OpenAI"""

	def __init__(self, client: AsyncOpenAI, model: str):
		self.client = client
		self.model = model

	async def generate(self, command: LLMCommand) -> LLMResultDTO:
		"""Генерация текста"""
		try:
			response = await self.client.chat.completions.create(
				model=self.model,
				messages=[
					{"role": "system", "content": command.prompt},
					{"role": "user", "content": command.input_text}
				],
				temperature=command.temperature
			)

			return LLMResultDTO(input_text=command.input_text, output_text=response.choices[0].message.content)

		except Exception as err:
			raise OpenAIServiceError(service="OpenAI", original_error=err, method="generate", prompt=command.prompt)
