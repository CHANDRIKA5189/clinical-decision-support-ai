from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_enabled: bool = False
    llm_base_url: str = "https://api.openai.com/v1"
    llm_api_key: str = ""
    llm_model: str = ""
    cors_origins: str = "http://localhost:5173"
    model_path: str = "app/models/disease_model.joblib"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
