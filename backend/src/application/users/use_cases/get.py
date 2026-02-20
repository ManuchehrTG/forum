from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.users.dtos import UserDTO
from src.application.users.queries import GetUserQuery, GetUserQueryType
from src.domain.users.entities.user import User
from src.domain.users.repository import UserRepository
from src.domain.users.value_objects import AuthProviderType

class GetUser:
	"""Единый use case для получения пользователя разными способами"""
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	@handle_domain_errors
	async def execute(self, query: GetUserQuery) -> UserDTO:
		"""Выполняет query и возвращает DTO"""

		if query.query_type == GetUserQueryType.BY_ID:
			user = await self._get_by_id(query.params["user_id"])

		elif query.query_type == GetUserQueryType.BY_PROVIDER_ID:
			provider_enum = AuthProviderType(query.params["provider"])

			user = await self._get_by_provider_id(provider_enum, query.params["provider_user_id"])

		else:
			raise ValueError(f"Unknown query type: {query.query_type}")

		return self._to_dto(user)

	async def _get_by_id(self, user_id: UUID) -> User:
		return await self.user_repo.get_by_id(user_id)

	async def _get_by_provider_id(self, provider: AuthProviderType, provider_user_id: str) -> User:
		return await self.user_repo.get_by_provider_user_id(provider, provider_user_id)

	def _to_dto(self, user: User) -> UserDTO:
		return UserDTO(
			id=user.id,
			first_name=user.first_name,
			last_name=user.last_name,
			username=user.username,
			about=user.about,
			location=user.location,
			birthday=user.birthday,
			language_code=user.language_code,
			avatar_path=user.avatar_path,
			email=user.email,
			phone=user.phone,
			created_at=user.created_at,
			updated_at=user.updated_at,
			# is_admin=user.is_admin,
		)
