from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    ADMIN_USER: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    
    model_config = SettingsConfigDict(env_file='.env')
    
settings = Settings()