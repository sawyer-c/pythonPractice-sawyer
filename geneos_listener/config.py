from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"

    # Optional shared secret for validating Geneos webhook requests.
    # Set via environment variable: GENEOS_WEBHOOK_SECRET=<your-secret>
    webhook_secret: str = ""

    model_config = {"env_prefix": "GENEOS_"}


settings = Settings()
