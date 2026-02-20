import uuid
from datetime import date, datetime
from typing import List

from .linked_account import LinkedAccount
from ..value_objects import AuthProviderType, Email, Phone
from src.core.config import settings

class User:
	def __init__(
		self,
		first_name: str,
		id: uuid.UUID | None = None,
		last_name: str | None = None,
		username: str | None = None,
		about: str | None = None,
		location: str | None = None,
		birthday: date | None = None,
		language_code: str = settings.app.default_language,
		avatar_path: str | None = None,
		email: str | None = None,
		phone: str | None = None,
		is_system: bool = False,
		is_admin: bool = False,
		created_at: datetime | None = None,
		updated_at: datetime | None = None,
		accounts: List[LinkedAccount] | None = None
	):
		self.id = id or uuid.uuid4()
		self.first_name = first_name
		self.last_name = last_name
		self.username = username
		self.about = about
		self.location = location
		self.birthday = birthday
		self.language_code = language_code if language_code in settings.app.languages else settings.app.default_language
		self.avatar_path = avatar_path

		self.email = email
		self.phone = phone

		self.is_system = is_system
		self.is_admin = is_admin

		self.created_at = created_at or datetime.utcnow()
		self.updated_at = updated_at or datetime.utcnow()

		self.accounts = accounts or []

	# Бизнес-методы
	@staticmethod
	def create_from_telegram(first_name: str, language_code: str | None, last_name: str | None, username: str | None) -> "User":
		return User(
			first_name=first_name,
			last_name=last_name,
			username=username,
			language_code=language_code or settings.app.default_language,
		)

	def add_linked_account(self, provider: AuthProviderType, provider_user_id: str, extra: dict):
		if any(acc.provider == provider for acc in self.accounts):
			raise ValueError(f"Account for provider {provider} already exists")

		linked_account = LinkedAccount(self.id, provider, provider_user_id, extra)
		self.accounts.append(linked_account)
		self.updated_at = datetime.utcnow()

	def update_profile(self, first_name: str, last_name: str | None, username: str | None, about: str | None, location: str | None, birthday: date | None):
		self.first_name = first_name
		self.last_name = last_name
		self.username = username
		self.about = about
		self.location = location
		self.birthday = birthday
		self.updated_at = datetime.utcnow()

	def update_avatar(self, avatar_path: str | None):
		self.avatar_path = avatar_path
		self.updated_at = datetime.utcnow()

	def update_linked_account(self):
		# Обновить данные в linked_account где provider == "telegram"
		self.updated_at = datetime.utcnow()

	@classmethod
	def from_db_record(cls, record: dict):
		return cls(
			id=record["id"],
			first_name=record["first_name"],
			last_name=record["last_name"],
			about=record["about"],
			location=record["location"],
			birthday=record["birthday"],
			language_code=record["language_code"],
			avatar_path=record["avatar_path"],
			# email=record["email"],
			# phone=record["phone"],
			is_system=record["is_system"],
			# is_admin=record["is_admin"],
			created_at=record["created_at"],
			updated_at=record["updated_at"],
		)

	@classmethod
	def from_db_with_accounts(cls, user_record: dict, account_records: List[dict]):
		user = cls.from_db_record(user_record)
		user.accounts = [LinkedAccount.from_db_record(account) for account in account_records]
		return user
