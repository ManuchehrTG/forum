from uuid import UUID

from src.application.decorators import handle_domain_errors
from src.application.users.commands import CreateUserCommand
from src.domain.users.entities.user import User
from src.domain.users.repository import UserRepository

class CreateUser:
	"""Создание нового пользователя"""
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	@handle_domain_errors
	async def execute(self, command: CreateUserCommand) -> UUID:
		user = User.create_from_telegram(
			first_name=command.first_name,
			last_name=command.last_name,
			username=command.username,
			language_code=command.language_code,
		)

		await self.user_repo.add(user)

		return user.id
