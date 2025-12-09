# class InvalidSectionError(MessageError):
# 	def __init__(self, section_code: str, allowed_sections: list[str]):
# 		self.section_code = section_code
# 		self.allowed_sections = allowed_sections
# 		super().__init__(
# 			f"Section `{section_code}` is not allowed. "
# 			f"Allowed sections: {', '.join(allowed_sections)}"
# 		)

# class MissingFieldForSectionError(MessageError):
# 	def __init__(self, field: str, section_code: str, required_sections: list[str]):
# 		self.field = field
# 		self.section_code = section_code
# 		self.required_sections = required_sections
# 		super().__init__(
# 			f"The `{field}` parameter is required for the `{section_code}` section."
# 		)
