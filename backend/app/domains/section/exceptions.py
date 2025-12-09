from app.core.exceptions import ValidationError

class InvalidSectionError(ValidationError):
	def __init__(self, section_code: str, allowed_sections: list[str]):
		super().__init__(
			message=f"Section `{section_code}` is not allowed. "
					f"Allowed sections: {', '.join(allowed_sections)}",
			field="section_code",
			section_code=section_code,
			allowed_sections=allowed_sections
		)

class MissingFieldForSectionError(ValidationError):
	def __init__(self, field: str, section_code: str, sections_requiring_field: list[str]):
		super().__init__(
			message=f"The `{field}` field is required when posting to `{section_code}` section. "
					f"Required for sections: {', '.join(sections_requiring_field)}",
			field=field,
			section_code=section_code,
			sections_requiring_field=sections_requiring_field
		)
