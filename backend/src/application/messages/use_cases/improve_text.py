from src.application.decorators import handle_domain_errors
from src.application.llm.commands import LLMCommand
from src.application.llm.dtos import LLMResultDTO
from src.domain.interfaces.llm_service import LLMService
from src.domain.sections.repository import SectionRepository

from src.application.messages.commands import MessageImproveTextCommand
from src.application.messages.dtos import MessageImproveTextDTO

class MessageImproveText:
	def __init__(self, section_repo: SectionRepository, llm_service: LLMService):
		self.section_repo = section_repo
		self.llm_service = llm_service

	@handle_domain_errors
	async def execute(self, command: MessageImproveTextCommand) -> MessageImproveTextDTO:
		section = await self.section_repo.get_by_id(command.section_id)
		section.ensure_ai_available()

		llm_command = LLMCommand(prompt=section.openai_prompt, input_text=command.text)			# pyright: ignore[reportArgumentType]
		llm_result = await self.llm_service.generate(llm_command)

		return self._to_dto(llm_result)

	def _to_dto(self, llm_result: LLMResultDTO):
		return MessageImproveTextDTO(
			input_text=llm_result.input_text,
			output_text=llm_result.output_text
		)
