from app.core.exceptions import NotFoundError
from app.core.security import verify_telegram, create_access_token, verify_jwt
from app.domains.user.schemas import User, UserCreateData, LinkedAccountCreateData
from app.domains.user.services import UserService, LinkedAccountService
from app.utils import download_telegram_avatar
from .exceptions import InvalidTMADataError
from .schemas import TelegramLoginRequest, TelegramData

class AuthService:
	def __init__(self, user_service: UserService, linked_account_service: LinkedAccountService):
		self.user_service = user_service
		self.linked_account_service = linked_account_service

	async def _telegram_auth(self, payload: TelegramLoginRequest) -> TelegramData:
		user_data = verify_telegram(init_data=payload.init_data)

		if not user_data:
			raise InvalidTMADataError()

		return TelegramData(**user_data)

	async def telegram_login(self, payload: TelegramLoginRequest) -> str:
		tg_user = await self._telegram_auth(payload)

		try:
			user = await self.user_service.get_user(user_id=tg_user.id, provider="telegram")
		except NotFoundError:
			avatar_url = await download_telegram_avatar(tg_user.photo_url, tg_user.id)
			user_data = UserCreateData(
				**tg_user.model_dump(),
				avatar_url=avatar_url["relative_path"]
				)
			user = await self.user_service.create_user(user_data=user_data)

			linked_account_data = LinkedAccountCreateData(
				user_id=user.id,
				provider="telegram",
				provider_user_id=tg_user.id,
				extra=tg_user.model_dump(exclude={"id"})
			)
			await self.linked_account_service.create_linked_account(linked_account_data=linked_account_data)

		return create_access_token({"sub": str(user.id), "provider": "telegram"})

	# async def telegram_link(self, user: User, payload: TelegramLoginRequest) -> str:
	# 	# TODO Проверить на повторное создание
	# 	tg_user = await self._telegram_auth(payload)

	# 	user_linked_account_data = UserLinkedAccountCreateData(
	# 		user_id=user.id,
	# 		provider="telegram",
	# 		provider_user_id=tg_user.id,
	# 		extra=tg_user.model_dump(exclude={"id"})
	# 	)

	# 	await self.user_service.create_user_linked_account(user_linked_account_data=user_linked_account_data)

	# 	return create_access_token({"sub": str(user.id), "provider": "telegram"})

	async def get_user_by_token(self, token: str) -> User:
		payload = verify_jwt(token=token)
		user_id = payload["sub"]

		return await self.user_service.get_user(user_id)
