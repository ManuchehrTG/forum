from asyncpg import Pool
from uuid import UUID

from src.domain.message_reactions.entities import MessageReaction
from src.domain.message_reactions.exceptions import MessageReactionNotFoundError
from src.domain.message_reactions.repository import MessageReactionRepository
from src.domain.message_reactions.value_objects import MessageReactionType, MessageReactionStats

class RawSQLMessageReactionRepository(MessageReactionRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def get_user_reaction(self, user_id: UUID, message_id: UUID) -> MessageReaction:
		async with self.pool.acquire() as connection:
			row = await connection.fetchrow(
				"""
				SELECT * FROM message_reactions
				WHERE user_id = $1 AND message_id = $2
				""",
				user_id, message_id
			)
			if not row:
				raise MessageReactionNotFoundError.by_user_and_message(user_id=user_id, message_id=message_id)

			return MessageReaction.from_db_record(row)

	async def upsert(self, user_id: UUID, message_id: UUID, reaction: MessageReactionType | None) -> MessageReaction | None:
		async with self.pool.acquire() as connection:
			if reaction is None:
				await connection.execute("DELETE FROM message_reactions WHERE user_id = $1 AND message_id = $2", user_id, message_id)
				return None

			else:
				row = await connection.fetchrow(
					"""
					INSERT INTO message_reactions (user_id, message_id, reaction, created_at, updated_at)
					VALUES ($1, $2, $3, NOW(), NOW())
					ON CONFLICT (user_id, message_id)
					DO UPDATE SET
						reaction = EXCLUDED.reaction,
						updated_at = CASE WHEN message_reactions.reaction != EXCLUDED.reaction THEN NOW() ELSE message_reactions.updated_at END
					RETURNING *
					""",
					user_id, message_id, reaction.value
				)

				return MessageReaction.from_db_record(row) if row else None

	async def get_stats(self, message_id: UUID) -> MessageReactionStats:
		async with self.pool.acquire() as connection:
			rows = await connection.fetch(
				"""
				SELECT reaction, COUNT(*) as count
				FROM message_reactions
				WHERE message_id = $1
				GROUP BY reaction
				ORDER BY count DESC, reaction
				""",
				message_id
			)
			return MessageReactionStats.from_db_rows(rows=rows)
