from infrastructure.llm import openai

class OpenAIService:
	async def generate_text(self, prompt: str, text: str, model: str = "gpt-4", temperature: float = 0.7) -> str | None:
		try:
			response = await openai.client.chat.completions.create(
				model=model,
				messages=[
					{"role": "system", "content": prompt},
					{"role": "user", "content": text}
				],
				temperature=temperature
			)
			new_text = response.choices[0].message.content
			return new_text
		except Exception as e:
			print("Error in OpenAIService [gpt-4]:", e)
			# raise OpenAIException(f"OpenAI error: {str(e)}")
