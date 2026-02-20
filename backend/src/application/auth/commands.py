from pydantic import BaseModel

class AuthByTelegramCommand(BaseModel):
	init_data: str
