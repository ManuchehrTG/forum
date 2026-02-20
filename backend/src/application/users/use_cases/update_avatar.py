from src.application.decorators import handle_domain_errors
from src.application.users.commands import UpdateUserAvatarCommand
from src.domain.users.repository import UserRepository
from src.domain.users.avatar_downloader import AvatarDownloader

class UpdateUserAvatar:
	def __init__(self, user_repo: UserRepository, avatar_downloader: AvatarDownloader):
		self.user_repo = user_repo
		self.avatar_downloader = avatar_downloader

	@handle_domain_errors
	async def execute(self, command: UpdateUserAvatarCommand) -> None:
		"""Обновляет аватар пользователя"""
		path = await self.avatar_downloader.download(
			provider=command.provider,
			photo_url=command.photo_url,
			user_id=command.user_id
		)

		if path:
			await self.user_repo.set_avatar(command.user_id, str(path))
