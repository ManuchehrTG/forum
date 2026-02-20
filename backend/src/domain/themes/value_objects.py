from uuid import UUID

class ThemeSection:
	def __init__(
		self,
		section_id: UUID,
		section_code: str,
		is_visible: bool = True,
	):
		self.section_id = section_id
		self.section_code = section_code
		self.is_visible = is_visible

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			section_id=record["section_id"],
			section_code=record["section_code"],
			is_visible=record["is_visible"]
		)
