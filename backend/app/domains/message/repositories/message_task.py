from typing import List, Tuple

from infrastructure.database import db
from ..schemas import MessageTask, MessageTaskCreateRequest, MessageWithTask

class MessageTaskRepository:
	@staticmethod
	async def create_message_task(data: MessageTaskCreateRequest, message_id: int) -> MessageTask:
		record = await db.fetchrow(
			"""
			INSERT INTO message_tasks (message_id, content_id, is_partially, expires_at)
			VALUES ($1, $2, $3, $4)
			RETURNING *
			""",
			message_id, data.content_id, data.is_partially, data.expires_at
		)
		return MessageTask(**record)

	@staticmethod
	async def get_message_with_tasks(theme_id: int, section_code: str, content_id: int, limit: int, offset: int) -> MessageWithTask:
		records = await db.fetch(
			"""
			SELECT
				row_to_json(m.*) as message_json,
				row_to_json(mt.*) as message_task_json
			FROM message_tasks mt
			JOIN messages m ON mt.message_id = m.id
			WHERE m.theme_id = $1 AND m.section_code = $2 AND mt.content_id = $3
			ORDER BY m.created_at DESC
			LIMIT $4 OFFSET $5
			""",
			theme_id, section_code, content_id, limit, offset
		)
		return [
			MessageWithTask.from_db_record(record=record)
			for record in records
		]
