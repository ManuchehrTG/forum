from app.core.exceptions import NotFoundError
from .repositories import SectionRepository
from .schemas import Section

class SectionService:
	async def get_section(self, section_code: str) -> Section:
		section = await SectionRepository.get_section_by_code(section_code=section_code)

		if not section:
			raise NotFoundError(entity="Section", entity_id=section_code)

		return section
