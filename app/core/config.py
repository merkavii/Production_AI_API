from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    max_file_size: int = 5 * 1024 * 1024
    chunk_size: int = 1024 * 1024
    
    allowed_types: list[str] = [
        "image/jpeg",
        "image/png"
    ]
    
    api_key : str
    
    database_password : str
    
    test_database_url: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )


settings = Settings()