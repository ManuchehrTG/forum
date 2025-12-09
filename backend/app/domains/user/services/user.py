from uuid import UUID

from app.core.exceptions import NotFoundError
from app.domains.auth.schemas import AuthProviderType
from ..repositories import UserRepository
from ..schemas import UserCreateData, User

class UserService:
	async def get_user(self, user_id: UUID, provider: AuthProviderType | None = None) -> User:
		if provider:
			user = await UserRepository.get_user_by_provider_user_id(provider_user_id=user_id, provider=provider)
		else:
			user = await UserRepository.get_user_by_id(user_id=user_id)

		if not user:
			raise NotFoundError(entity="User", entity_id=user_id)

		return user

	async def create_user(self, user_data: UserCreateData) -> User:
		return await UserRepository.create_user(data=user_data)
