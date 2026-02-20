from src.application.decorators import handle_domain_errors
from src.application.auth.commands import AuthByTelegramCommand
from src.application.auth.dtos import AuthResultDTO
from src.application.auth.exceptions import AuthFailedError
from src.domain.users.entities.user import User
from src.domain.users.exceptions import UserNotFoundError
from src.domain.users.avatar_downloader import AvatarDownloader
from src.domain.users.repository import UserRepository
from src.domain.users.value_objects import AuthProviderType
from src.infrastructure.auth.jwt import JWTManager
from src.infrastructure.auth.telegram import TelegramInitDataValidator, TelegramUserData

class AuthByTelegram:
	def __init__(self, user_repo: UserRepository, tg_validator: TelegramInitDataValidator, avatar_downloader: AvatarDownloader):
		self.user_repo = user_repo
		self.tg_validator = tg_validator
		self.avatar_downloader = avatar_downloader

	@handle_domain_errors
	async def execute(self, command: AuthByTelegramCommand) -> AuthResultDTO:
		try:
			tg_user: TelegramUserData = self.tg_validator.validate(command.init_data)
		except Exception:
			raise AuthFailedError("Invalid Telegram initData")

		provider = AuthProviderType.TELEGRAM

		try:
			user = await self.user_repo.get_by_provider_user_id(provider, str(tg_user.id))
			user.update_linked_account()
			# TODO
			# await self.user_repo.update_linked_account(user)

		except UserNotFoundError:
			user = User.create_from_telegram(
				first_name=tg_user.first_name,
				last_name=tg_user.last_name,
				username=tg_user.username,
				language_code=tg_user.language_code
			)
			user.add_linked_account(
				provider=provider,
				provider_user_id=str(tg_user.id),
				extra=tg_user.model_dump()
			)
			await self.user_repo.add(user)

		if not user.avatar_path and tg_user.photo_url:
			avatar_path = await self.avatar_downloader.download(
				provider=provider,
				photo_url=tg_user.photo_url,
				user_id=user.id
			)
			if avatar_path:
				await self.user_repo.set_avatar(user.id, avatar_path)

		access_token = JWTManager.create_access_token({"sub": str(tg_user.id), "provider": "telegram"})
		refresh_token = JWTManager.create_refresh_token(tg_user.id)

		return AuthResultDTO(access_token=access_token, refresh_token=refresh_token)
