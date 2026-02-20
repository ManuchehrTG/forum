from src.core.config import settings
from src.domain.users.entities import User
from src.domain.users.exceptions import UserNotFoundError
from src.domain.users.repository import UserRepository

USERS = [
	{
		"id": settings.system_user_id,
		"first_name": "System",
		"is_system": True
	}
]

async def seed_users(user_repo: UserRepository):
	for item in USERS:
		try:
			await user_repo.get_by_id(item["id"])
			continue
		except UserNotFoundError:
			user = User(**item)
			await user_repo.add(user)
