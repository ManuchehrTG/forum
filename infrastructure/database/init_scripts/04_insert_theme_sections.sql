INSERT INTO theme_sections (theme_id, section_code)
VALUES ($1, $2)
ON CONFLICT (theme_id, section_code) DO NOTHING;