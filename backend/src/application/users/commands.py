import uuid
from datetime import date
from pydantic import BaseModel
from src.domain.users.value_objects import AuthProviderType

class CreateUserCommand(BaseModel):
	first_name: str
	last_name: str | None = None
	username: str | None = None
	language_code: str
	avatar_path: str | None = None

	is_admin: bool = False

class UpdateUserProfileCommand(BaseModel):
	user_id: uuid.UUID
	first_name: str
	last_name: str | None = None
	username: str | None = None
	about: str | None = None
	location: str | None = None
	birthday: date | None = None

class UpdateUserAvatarCommand(BaseModel):
	user_id: uuid.UUID
	photo_url: str
	provider: AuthProviderType
