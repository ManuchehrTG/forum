from fastapi import Depends, HTTPException

from .factory import create_section_service
from .schemas import Section
from .services import SectionService

def get_section_service() -> SectionService:
	return create_section_service()

async def get_section(
	section_code: str,
	section_service: SectionService = Depends(get_section_service)
) -> Section:
	return await section_service.get_section(section_code=section_code)
