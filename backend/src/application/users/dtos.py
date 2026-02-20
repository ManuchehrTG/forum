import uuid
from datetime import date, datetime

from pydantic import BaseModel

class UserDTO(BaseModel):
	id: uuid.UUID

	first_name: str
	last_name: str | None = None
	username: str | None = None
	about: str | None = None
	location: str | None = None
	birthday: date | None = None
	language_code: str
	avatar_path: str | None = None

	email: str | None = None
	phone: str | None = None

	created_at: datetime
	updated_at: datetime

	# is_admin: bool
