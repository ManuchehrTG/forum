from .schemas import Theme, ThemeResponse

def theme_to_response(theme: Theme) -> ThemeResponse:
	return ThemeResponse(**theme.model_dump())
