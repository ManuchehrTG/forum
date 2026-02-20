from uuid import UUID

from src.shared.exceptions import NotFoundError, BusinessRuleError

class MediaFileNotFoundError(NotFoundError):
	"""Медиафайл не найден"""
	error_code = "media_file_not_found"

	def __init__(self, media_file_id: str | UUID, search_type: str, **kwargs):
		super().__init__(entity="MediaFile", entity_id=str(media_file_id), search_type=search_type, **kwargs)

	@classmethod
	def by_id(cls, media_file_id: str | UUID, **kwargs) -> "MediaFileNotFoundError":
		return cls(media_file_id=media_file_id, search_type="id", **kwargs)

	@classmethod
	def by_path(cls, path: str, **kwargs) -> "MediaFileNotFoundError":
		return cls(media_file_id=path, search_type="path", **kwargs)


class MediaFileStateConflictError(BusinessRuleError):
	"""Медиафайл в неправильном состоянии для операции"""
	error_code = "media_file_state_conflict"

	@classmethod
	def incorrect_is_temp(cls, media_file_id: str | UUID, **kwargs):
		return cls(
			message=f"MediaFile {media_file_id} is not temporary",
			code="media_file_state_conflict.incorrect_is_temp",
			details={
				"media_file_id": str(media_file_id),
				"reason": "wrong_is_temp"
			},
			**kwargs
		)
