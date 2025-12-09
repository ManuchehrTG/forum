from typing import List, Tuple

from infrastructure.database import db
from ..schemas import MessagePost, MessagePostCreateRequest, MessageWithPost

class MessagePostRepository:
	@staticmethod
	async def create_message_post(data: MessagePostCreateRequest, message_id: int) -> MessagePost:
		record = await db.fetchrow(
			"""
			INSERT INTO message_posts (message_id, is_openai_generated, ratio)
			VALUES ($1, $2, $3)
			RETURNING *
			""",
			message_id, data.is_openai_generated, data.ratio
		)
		return MessagePost(**record)

	@staticmethod
	async def get_message_with_posts(theme_id: int, section_code: str, limit: int, offset: int) -> List[MessageWithPost]:
		records = await db.fetch(
			"""
			SELECT
				row_to_json(m.*) as message_json,
				row_to_json(mp.*) as message_post_json
			FROM message_posts mp
			JOIN messages m ON mp.message_id = m.id
			WHERE m.theme_id = $1 AND m.section_code = $2
			ORDER BY m.created_at DESC
			LIMIT $3 OFFSET $4
			""",
			theme_id, section_code, limit, offset
		)
		return [
			MessageWithPost.from_db_record(record=record)
			for record in records
		]
