from infrastructure.database import db

class MessageCRUD:
	@staticmethod
	async def create(author_id: int, theme_id: int, section_key: str, text: str, type: str):
		return await db.fetchrow(
			"""
			INSERT INTO messages (author_id, theme_id, section_key, text, type)
			VALUES ($1, $2, $3, $4, $5)
			RETURNING *
			""",
			author_id, theme_id, section_key, text, type
		)

	@staticmethod
	async def add_attachment(message_id: int, attachment_id: int, sort_order: int):
		await db.fetchrow(
			"""
			INSERT INTO message_attachments (message_id, attachment_id, sort_order)
			VALUES ($1, $2, $3)
			""",
			message_id, attachment_id, sort_order
		)

	@staticmethod
	async def get_by_id(
		user_id: int,
		message_id: int,
		theme_id: int,
		section_key: str,
		include_attachments: bool = True,
		include_reactions: bool = True
	):	# TODO:
		# - Поправить, чтобы код работал с параметрами include_attachments и include_reactions
		return await db.fetchrow(
			"""
			SELECT
				m.id AS id,
				m.section_key AS section_key,
				m.text AS text,
				m.type AS type,
				m.created_at AS created_at,
				m.updated_at AS updated_at,
				-- Автор
				json_build_object(
					'id', u.id,
					'username', u.username,
					'first_name', u.first_name,
					'last_name', u.last_name,
					'avatar_url', u.avatar_url,
					'language_code', u.language_code
				) AS author,
				-- Вложения
				COALESCE(
					json_agg(
						json_build_object(
							'id', f.id,
							'stored_path', f.stored_path,
							'original_name', f.original_name,
							'mime_type', f.mime_type,
							'size', f.size,
							'metadata', f.metadata,
							'created_at', f.created_at,
							'updated_at', f.updated_at
						) ORDER BY ma.sort_order ASC
					) FILTER (WHERE f.id IS NOT NULL),
					'[]'::json
				) AS attachments,
				-- Реакции
				json_build_object(
					'count_likes', COALESCE(SUM(CASE WHEN r.reaction = 'like' THEN 1 ELSE 0 END), 0),
					'count_dislikes', COALESCE(SUM(CASE WHEN r.reaction = 'dislike' THEN 1 ELSE 0 END), 0),
					'user_reaction', MAX(CASE WHEN r.user_id = $1 THEN r.reaction ELSE NULL END)
				) AS reactions
			FROM messages m
			JOIN users u ON u.id = m.author_id
			LEFT JOIN message_attachments ma ON ma.message_id = m.id
			LEFT JOIN files f ON f.id = ma.attachment_id
			LEFT JOIN reactions r ON r.message_id = m.id
			WHERE m.id = $2 AND m.theme_id = $3 AND m.section_key = $4
			GROUP BY m.id, u.id
			""",
			user_id, message_id, theme_id, section_key
		)

	@staticmethod
	async def get_reactions_by_message_id_and_user_id(message_id: int):
		return await db.fetchrow(
			"""
			SELECT
				COALESCE(SUM(CASE WHEN reaction = 'like' THEN 1 ELSE 0 END), 0) AS count_likes,
				COALESCE(SUM(CASE WHEN reaction = 'dislike' THEN 1 ELSE 0 END), 0) AS count_dislikes
			FROM reactions
			WHERE message_id = $1
			""",
			message_id
		)

	@staticmethod
	async def get_reaction_by_message_id_and_user_id(message_id: int, user_id: int):
		return await db.fetchrow("SELECT * FROM reactions WHERE message_id = $1 AND user_id = $2", message_id, user_id)

	@staticmethod
	async def update_reaction(message_id: int, user_id: int, reaction: str):
		return await db.fetchrow(
			"""
			INSERT INTO reactions (message_id, user_id, reaction)
			VALUES ($1, $2, $3)
			ON CONFLICT (message_id, user_id)
			DO UPDATE SET
				reaction = EXCLUDED.reaction,
				updated_at = now()
			RETURNING *
			""",
			message_id, user_id, reaction
		)

	@staticmethod
	async def get_reaction_counts_by_message_id(message_id: int):
		return await db.fetchrow(
			"""
			SELECT
				COALESCE(SUM(CASE WHEN reaction = 'like' THEN 1 ELSE 0 END), 0) AS count_likes,
				COALESCE(SUM(CASE WHEN reaction = 'dislike' THEN 1 ELSE 0 END), 0) AS count_dislikes
			FROM reactions
			WHERE message_id = $1
			""",
			message_id
		)
