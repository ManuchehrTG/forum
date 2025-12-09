from app.core.exceptions import AppError

class AIFeatureDisabledError(AppError):
	"""AI-функциональность отключена в разделе"""
	def __init__(self, section_code: str):
		super().__init__(
			message=f"AI features are disabled in `{section_code}` section",
			code="ai_features_disabled",
			status_code=403,
			section_code=section_code
		)
