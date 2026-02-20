from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.sections.dtos import SectionDTO
from src.application.sections.queries import GetSectionQuery, GetSectionQueryType
from src.domain.sections.entities import Section
from src.domain.sections.repository import SectionRepository

class GetSection:
	"""Единый use case для получения пользователя разными способами"""
	def __init__(self, section_repo: SectionRepository):
		self.section_repo = section_repo

	@handle_domain_errors
	async def execute(self, query: GetSectionQuery) -> SectionDTO:
		"""Выполняет query и возвращает DTO"""

		if query.query_type == GetSectionQueryType.BY_ID:
			section = await self._get_by_id(query.params["section_id"])

		elif query.query_type == GetSectionQueryType.BY_CODE:
			section = await self._get_by_code(query.params["section_code"])

		else:
			raise ValueError(f"Unknown query type: {query.query_type}")

		return self._to_dto(section)

	async def _get_by_id(self, section_id: UUID) -> Section:
		return await self.section_repo.get_by_id(section_id)

	async def _get_by_code(self, section_code: str) -> Section:
		return await self.section_repo.get_by_code(section_code)

	def _to_dto(self, section: Section) -> SectionDTO:
		return SectionDTO(
			id=section.id,
			code=section.code,
			openai_prompt=section.openai_prompt,
			tech_version=section.tech_version,
			enable_openai=section.enable_openai,
			allow_hide=section.allow_hide,
			created_at=section.created_at,
			updated_at=section.updated_at,
		)
