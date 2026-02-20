# НЕ ИСПОЛЬЗУЕТСЯ

# from .use_cases.create import CreateUser
# from .use_cases.get import GetUser
# from .use_cases.update_profile import UpdateUserProfile
# from .use_cases.update_avatar import UpdateUserAvatar
# from src.domain.users.repository import UserRepository
# from src.domain.users.avatar_downloader import AvatarDownloader

# class UsersUseCaseFactory:
# 	"""Фабрика use cases ТОЛЬКО для users bounded context"""
# 	def __init__(self, user_repo: UserRepository, avatar_downloader: AvatarDownloader):
# 		self.user_repo = user_repo
# 		self.avatar_downloader = avatar_downloader

# 	def create_user(self) -> CreateUser:
# 		return CreateUser(user_repo=self.user_repo)

# 	def get_user(self) -> GetUser:
# 		return GetUser(user_repo=self.user_repo)

# 	def update_profile(self) -> UpdateUserProfile:
# 		return UpdateUserProfile(user_repo=self.user_repo)

# 	def update_avatar(self) -> UpdateUserAvatar:
# 		return UpdateUserAvatar(user_repo=self.user_repo, avatar_downloader=self.avatar_downloader)
