from typing import List, Tuple

from infrastructure.database import db
from ..schemas import MessageComment, MessageCommentCreateRequest, MessageWithComment

class MessageCommentRepository:
	@staticmethod
	async def create_message_comment(data: MessageCommentCreateRequest, message_id: int) -> MessageComment:
		record = await db.fetchrow(
			"""
			INSERT INTO message_comments (message_id, content_id, reply_to_message_id)
			VALUES ($1, $2, $3)
			RETURNING *
			""",
			message_id, data.content_id, data.reply_to_message_id
		)
		return MessageComment(**record)

	@staticmethod
	async def get_message_with_comments(theme_id: int, section_code: str, content_id: int, limit: int, offset: int) -> MessageWithComment:
		records = await db.fetch(
			"""
			SELECT
				row_to_json(m.*) as message_json,
				row_to_json(mc.*) as message_comment_json
			FROM message_comments mc
			JOIN messages m ON mc.message_id = m.id
			WHERE m.theme_id = $1 AND m.section_code = $2 AND mc.content_id = $3
			ORDER BY m.created_at DESC
			LIMIT $4 OFFSET $5
			""",
			theme_id, section_code, content_id, limit, offset
		)
		return [
			MessageWithComment.from_db_record(record=record)
			for record in records
		]
