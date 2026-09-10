from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    APP_NAME: str = "HelpDesk"

    # Pydantic должен читать значения из файла .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# экземпляр класса, который автоматически подтянет данные
settings = Settings()