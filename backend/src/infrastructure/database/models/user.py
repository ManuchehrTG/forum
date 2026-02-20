from datetime import date
from sqlalchemy import Boolean, Date, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from src.infrastructure.database.base import Base, TimestampMixin
# from .linked_account import LinkedAccountModel

class UserModel(Base, TimestampMixin):
	__tablename__ = "users"

	first_name: Mapped[str] = mapped_column(String(32), nullable=False)
	last_name: Mapped[str | None] = mapped_column(String(32), nullable=True)
	username: Mapped[str | None] = mapped_column(String(32), unique=True, nullable=True)
	about: Mapped[str | None] = mapped_column(Text, nullable=True)
	location: Mapped[str | None] = mapped_column(Text, nullable=True)
	birthday: Mapped[date | None] = mapped_column(Date, nullable=True)

	email: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
	phone: Mapped[str | None] = mapped_column(String(16), unique=True, nullable=True)

	language_code: Mapped[str] = mapped_column(String(5), nullable=False)
	avatar_path: Mapped[str | None] = mapped_column(Text, nullable=True)

	is_system: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

	# linked_accounts: Mapped[List[LinkedAccountModel]] = relationship(LinkedAccountModel, cascade="all, delete-orphan")
