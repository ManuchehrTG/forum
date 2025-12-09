from asyncpg import Record
from typing import List
from uuid import UUID

from infrastructure.database import db
from app.domains.media_file.schemas import MediaFile
from ..schemas import Message, MessageCreateRequest, MessageReaction, MessageReactionType

class MessageRepository:
	@staticmethod
	async def create_message(data: MessageCreateRequest, author_id: UUID, theme_id: int, section_code: str) -> Message:
		record = await db.fetchrow(
			"""
			INSERT INTO messages (author_id, theme_id, section_code, text, type)
			VALUES ($1, $2, $3, $4, $5)
			RETURNING *
			""",
			author_id, theme_id, section_code, data.text, data.type
		)
		return Message(**record)

	@staticmethod
	async def get_message_by_id(message_id: int) -> Message | None:
		record = await db.fetchrow("SELECT * FROM messages WHERE id = $1", message_id)
		if record:
			return Message(**record)

	@staticmethod
	async def create_message_files(media_files: List[MediaFile], message_id: int) -> None:
		data = [(message_id, media_file.id, i) for i, media_file in enumerate(media_files, 1)]
		await db.executemany("INSERT INTO message_files (message_id, media_file_id, sort_order) VALUES ($1, $2, $3)", data)

	@staticmethod
	async def get_message_file_ids(message_id: int) -> List[UUID]:
		records = await db.fetch("SELECT media_file_id FROM message_files WHERE message_id = $1 ORDER BY sort_order ASC", message_id)
		return [record["media_file_id"] for record in records]

	@staticmethod
	async def update_message_reaction(user_id: UUID, message_id: int, reaction: MessageReactionType) -> None:
		await db.execute(
			"""
			INSERT INTO message_reactions (message_id, user_id, reaction)
			VALUES ($1, $2, $3)
			ON CONFLICT (message_id, user_id)
			DO UPDATE SET
				reaction = EXCLUDED.reaction,
				updated_at = now()
			WHERE message_reactions.reaction != EXCLUDED.reaction
			""",
			message_id, user_id, reaction
		)

	@staticmethod
	async def get_message_reactions(message_id: int) -> List[MessageReaction]:
		records = await db.fetch("SELECT * FROM message_reactions WHERE message_id = $1", message_id)
		return [MessageReaction(**record) for record in records]
