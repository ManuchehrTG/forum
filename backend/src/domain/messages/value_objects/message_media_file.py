from uuid import UUID

class MessageMediaFile:
	def __init__(
		self,
		media_file_id: UUID,
		sort_order: int
	):
		self.media_file_id = media_file_id
		self.sort_order = sort_order

	def to_dict(self) -> dict:
		return {
			"media_file_id": self.media_file_id,
			"sort_order": self.sort_order
		}

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			media_file_id=record["media_file_id"],
			sort_order=record["sort_order"],
		)
