from pydantic_settings import BaseSettings

class ProxySettings(BaseSettings):
	http: str
	socks5: str

	class Config:
		env_prefix = "PROXY_"
		case_sensitive = False
