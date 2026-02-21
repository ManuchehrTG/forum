from asyncpg import Pool
from typing import List
from uuid import UUID

from src.domain.messages.entities import Message
from src.domain.messages.exceptions import MessageNotFoundError
from src.domain.messages.repository import MessageRepository
from src.domain.messages.value_objects import MessageType

class RawSQLMessageRepository(MessageRepository):
	def __init__(self, pool: Pool):
		self.pool = pool

	async def get_by_id(self, message_id: UUID) -> Message:
		async with self.pool.acquire() as connection:
			query = """
			WITH message_media AS (
				SELECT 
					message_id,
					json_agg(mmf) as media_files
				FROM message_media_files mmf
				WHERE message_id = $1
				GROUP BY message_id
			)
			SELECT 
				m.*,
				pmd as post_message_data,
				tmd as task_message_data,
				tamd as task_assignment_message_data,
				cmd as comment_message_data,
				COALESCE(mm.media_files, '[]'::json) as message_media_files
			FROM messages m
			LEFT JOIN post_message_data pmd ON m.id = pmd.message_id
			LEFT JOIN task_message_data tmd ON m.id = tmd.message_id
			LEFT JOIN task_assignment_message_data tamd ON m.id = tamd.message_id
			LEFT JOIN comment_message_data cmd ON m.id = cmd.message_id
			LEFT JOIN message_media mm ON m.id = mm.message_id
			WHERE m.id = $1
			"""
			row = await connection.fetchrow(query, message_id)

			if not row:
				raise MessageNotFoundError.by_id(message_id)

			return Message.from_db_record_with_data_and_media(row)

	async def save(self, message: Message) -> None:
		async with self.pool.acquire() as connection:
			async with connection.transaction():
				await connection.execute(
					"""
					INSERT INTO messages(id, author_id, theme_id, section_id, type, text, is_openai_generated, created_at, updated_at)
					VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
					ON CONFLICT (id) DO UPDATE SET
						text = EXCLUDED.text,
						is_openai_generated = EXCLUDED.is_openai_generated,
						updated_at = EXCLUDED.updated_at
					""",
					message.id, message.author_id, message.theme_id, message.section_id, message.type.value, message.text, message.is_openai_generated,
					message.created_at, message.updated_at
				)

				await self._save_specific_data(connection, message)

				await connection.execute("DELETE FROM message_media_files WHERE message_id = $1", message.id)

				for mf in message.media_files:
					await connection.execute(
						"""
						INSERT INTO message_media_files (message_id, media_file_id, sort_order)
						VALUES ($1, $2, $3)
						""",
						message.id, mf.media_file_id, mf.sort_order
					)

	async def _save_specific_data(self, connection, message: Message) -> None:
		"""Сохраняет специфичные данные в соответствующие таблицы"""

		if message.type == MessageType.POST and message.task_data:
			await connection.execute(
				"""
				INSERT INTO post_message_data (message_id)
				VALUES ($1)
				ON CONFLICT (id) DO NOTHING
				""",
				message.id
			)

		elif message.type == MessageType.TASK and message.task_data:
			await connection.execute(
				"""
				INSERT INTO task_message_data (message_id, ratio)
				VALUES ($1, $2)
				ON CONFLICT (id) DO UPDATE SET
					ratio = EXCLUDED.ratio
				""",
				message.id, message.task_data.ratio
			)

		elif message.type == MessageType.TASK_ASSIGNMENT and message.task_assignment_data:
			await connection.execute(
				"""
				INSERT INTO task_assignment_message_data (message_id, content_id, is_partially, status, expires_at)
				VALUES ($1, $2, $3, $4, $5)
				ON CONFLICT (id) DO UPDATE SET
					is_partially = EXCLUDED.is_partially,
					status = EXCLUDED.status,
					expires_at = EXCLUDED.expires_at
				""",
				message.id,
				message.task_assignment_data.content_id,
				message.task_assignment_data.is_partially,
				message.task_assignment_data.status.value,
				message.task_assignment_data.expires_at
			)

		elif message.type == MessageType.COMMENT and message.comment_data:
			await connection.execute(
				"""
				INSERT INTO comment_message_data (message_id, content_id, reply_to_message_id)
				VALUES ($1, $2, $3)
				ON CONFLICT (id) DO NOTHING
				""",
				message.id,
				message.comment_data.content_id,
				message.comment_data.reply_to_message_id
			)

	async def get_list(self, type: MessageType, theme_id: UUID, section_id: UUID, content_id: UUID | None = None, limit: int = 10, offset: int = 0) -> List[Message]:
		async with self.pool.acquire() as connection:
			query = """
			SELECT 
				m.*,
				pmd as post_message_data,
				tmd as task_message_data,
				tamd as task_assignment_message_data,
				cmd as comment_message_data,
				(
					SELECT COALESCE(json_agg(mmf), '[]'::json)
					FROM message_media_files mmf
					WHERE mmf.message_id = m.id
				) as message_media_files
			FROM messages m
			LEFT JOIN post_message_data pmd ON m.id = pmd.message_id
			LEFT JOIN task_message_data tmd ON m.id = tmd.message_id
			LEFT JOIN task_assignment_message_data tamd ON m.id = tamd.message_id
			LEFT JOIN comment_message_data cmd ON m.id = cmd.message_id
			WHERE m.theme_id = $1 AND m.section_id = $2 AND m.type = $3
			"""

			params: list = [theme_id, section_id, type.value]

			if content_id is not None:
				query += " AND COALESCE(tamd.content_id, cmd.content_id) = $4"
				query += " ORDER BY m.created_at DESC LIMIT $5 OFFSET $6"
				params.append(content_id)
			else:
				query += " ORDER BY m.created_at DESC LIMIT $4 OFFSET $5"

			params.extend([limit, offset])

			rows = await connection.fetch(query, *params)

			return [Message.from_db_record_with_data_and_media(row) for row in rows]

