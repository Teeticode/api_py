from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_PASSWORD: str 
    DATABASE_USERNAME: str 
    SECRET_KEY: str 
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    algorithm: str
    access_token_expire_min: int

    class Config:
        env_file = ".env"


settings = Settings()
