from app.core.exceptions import AuthError

class TokenExpiredError(AuthError):
	def __init__(self):
		super().__init__(
			message="Token has expired",
			code="token_expired",
			headers={"WWW-Authenticate": "Bearer error=`invalid_token`, error_description=`The access token expired`"}
		)

class InvalidTokenError(AuthError):
	def __init__(self):
		super().__init__(
			message="Invalid token",
			code="invalid_token",
			headers={"WWW-Authenticate": "Bearer error=`invalid_token`"}
		)

class InvalidTMADataError(AuthError):
	def __init__(self):
		super().__init__(
			message="Invalid Telegram Mini App data",
			code="invalid_telegram_mini_app_data",
		)

class ExpiredTelegramDataError(AuthError):
	def __init__(self):
		super().__init__(
			message="Expired Telegram Mini App data",
			code="expired_telegram_mini_app_data",
		)
