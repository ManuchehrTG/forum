INSERT INTO sections (code, openai_prompt, allow_hide, tech_version)
VALUES ($1, $2, $3, $4)
ON CONFLICT (code) DO NOTHING;
