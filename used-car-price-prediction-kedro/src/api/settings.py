from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MODEL_PATH: str | None = None
    WANDB_API_KEY: str | None = None
    API_URL: str | None = None
    DATABASE_URL: str = "sqlite:///./data/08_reporting/api_predictions.db"

    model_config = SettingsConfigDict(env_file=".env")
