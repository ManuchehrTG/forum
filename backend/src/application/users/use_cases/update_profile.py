from src.application.decorators import handle_domain_errors
from src.application.users.commands import UpdateUserProfileCommand
from src.domain.users.repository import UserRepository

class UpdateUserProfile:
	"""Обновление профиля пользователя"""
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	@handle_domain_errors
	async def execute(self, command: UpdateUserProfileCommand) -> None:
		user = await self.user_repo.get_by_id(command.user_id)

		# Бизнес-логика обновления
		user.update_profile(
			first_name=command.first_name,
			last_name=command.last_name,
			username=command.username,
			about=command.about,
			location=command.location,
			birthday=command.birthday
		)

		await self.user_repo.update(user)
