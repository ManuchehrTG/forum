-- DELETE TABLE
-- DROP TABLE IF EXISTS message_files, media_files, message_reactions, message_tasks, message_comments, message_posts, messages, theme_sections, sections, themes, ratings, linked_accounts, users;
-- DROP TABLE message_reactions;

-- CREATE TABLE
CREATE TABLE IF NOT EXISTS users (
	id						UUID						PRIMARY KEY DEFAULT gen_random_uuid(),
	first_name				TEXT,
	username				TEXT						UNIQUE,
	email					TEXT						UNIQUE,
	phone_number			TEXT						UNIQUE,
	language_code			TEXT,
	avatar_url				TEXT,
	negative_points			BIGINT						DEFAULT 0,
	positive_points			BIGINT						DEFAULT 0,
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS linked_accounts (
	id						UUID						PRIMARY KEY DEFAULT gen_random_uuid(),
	user_id					UUID						NOT NULL REFERENCES users(id),
	provider				TEXT						NOT NULL,
	provider_user_id		TEXT,
	extra					JSONB						DEFAULT '{}',
	UNIQUE (provider, provider_user_id)
);

-- CREATE TABLE IF NOT EXISTS ratings (
-- 	user_id					UUID						PRIMARY KEY REFERENCES users(id),
-- 	n_points				BIGINT						DEFAULT 0,
-- 	p_points				BIGINT						DEFAULT 0
-- );

CREATE TABLE IF NOT EXISTS themes (
	id						SERIAL						PRIMARY KEY,
	parent_id				INT							REFERENCES themes(id),
	author_id				UUID						REFERENCES users(id),
	title					VARCHAR(32)					NOT NULL UNIQUE,
	is_group				BOOL						DEFAULT FALSE,
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS sections (
	code					TEXT						PRIMARY KEY,
	is_openai_enabled		BOOL						DEFAULT TRUE,
	openai_prompt			TEXT,
	allow_hide				BOOL						DEFAULT TRUE,
	tech_version			TEXT
);

CREATE TABLE IF NOT EXISTS theme_sections (
	id						UUID						PRIMARY KEY DEFAULT gen_random_uuid(),
	theme_id				INT							NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
	section_code			TEXT						NOT NULL REFERENCES sections(code) ON DELETE CASCADE,
	is_visible				BOOLEAN						NOT NULL DEFAULT TRUE,
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	UNIQUE(theme_id, section_code)
);

CREATE TABLE IF NOT EXISTS messages (
	id						BIGSERIAL					PRIMARY KEY,
	author_id				UUID						NOT NULL REFERENCES users(id),
	theme_id				INT							NOT NULL REFERENCES themes(id) ON DELETE CASCADE,
	section_code			TEXT						NOT NULL REFERENCES sections(code) ON DELETE CASCADE,
	text					TEXT,
	type					TEXT						CHECK (type IN ('post', 'comment', 'task')) DEFAULT 'post',
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS message_posts (
	message_id				BIGINT						PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
	is_openai_generated		BOOLEAN						DEFAULT FALSE,
	ratio					INT
);

CREATE TABLE IF NOT EXISTS message_comments (
	message_id				BIGINT						PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
	content_id				BIGINT						REFERENCES messages(id) ON DELETE CASCADE,
	reply_to_message_id		BIGINT						REFERENCES message_comments(message_id) -- ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS message_tasks (
	message_id				BIGINT						PRIMARY KEY REFERENCES messages(id) ON DELETE CASCADE,
	content_id				BIGINT						REFERENCES messages(id) ON DELETE CASCADE,
	is_partially			BOOLEAN						DEFAULT FALSE,
	status					TEXT						CHECK (status IN ('in_progress', 'successful', 'failed')) DEFAULT 'in_progress',
	expires_at				TIMESTAMP					WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS message_reactions (
	id						BIGSERIAL					PRIMARY KEY,
	message_id				BIGINT						REFERENCES messages(id) ON DELETE CASCADE,
	user_id					UUID						REFERENCES users(id),
	reaction				TEXT,
	-- points				INT,
	-- voice_multiplier		INT,
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	UNIQUE (user_id, message_id)
);

CREATE TABLE IF NOT EXISTS media_files (
	id						UUID						PRIMARY KEY DEFAULT gen_random_uuid(),
	author_id				UUID						REFERENCES users(id),
	file_path				TEXT						NOT NULL UNIQUE,
	original_name			TEXT						NOT NULL,
	mime_type				TEXT						NOT NULL,
	file_size				BIGINT						NOT NULL,
	status					TEXT						CHECK (status IN ('temporary', 'attached')),
	metadata				JSONB						DEFAULT '{}',
	expires_at				TIMESTAMP					WITH TIME ZONE,
	created_at				TIMESTAMP					WITH TIME ZONE DEFAULT now(),
	updated_at				TIMESTAMP					WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS message_files (
	message_id				BIGINT						REFERENCES messages(id) ON DELETE CASCADE,
	media_file_id			UUID						REFERENCES media_files(id) ON DELETE CASCADE,
	sort_order				INT							DEFAULT 0,
	PRIMARY KEY (message_id, media_file_id)
);

-- CREATE TABLE IF NOT EXISTS switches (
-- 	id						SERIAL						PRIMARY KEY,
-- 	mark					TEXT						UNIQUE,
-- 	is_on					BOOL						DEFAULT TRUE,
-- 	date_update				TIMESTAMP					WITH TIME ZONE DEFAULT now()
-- );
