from pydantic_settings import BaseSettings

class StorageSettings(BaseSettings):
	dir: str

	@property
	def avatar_dir(self) -> str:
		return f"{self.dir}/avatars"

	class Config:
		env_prefix = "STORAGE_"
		case_sensitive = False
