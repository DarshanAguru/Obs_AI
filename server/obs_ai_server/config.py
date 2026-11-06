import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Obs_AI Server"
    app_version: str = "0.0.1"

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = "sqlite:///./obs_ai.db"
    redis_url: str = "redis://localhost:6379/0"

    max_batch_size: int = 100
    max_payload_size: int = 10 * 1024 * 1024  # 10 MB

    log_level: str = "INFO"
    retention_days: int = 30
    sample_rate: float = 1.0

    model_config = SettingsConfigDict(
        env_prefix="OBS_AI_",
        env_file=".env",
        extra="ignore",
    )

    def __init__(self, **values):
        super().__init__(**values)
        # Backward compatibility for AI_OBS_* and FEENION_* environment variables
        for key in ["database_url", "redis_url", "log_level", "retention_days", "host", "port"]:
            legacy_val = os.getenv(f"AI_OBS_{key.upper()}") or os.getenv(f"FEENION_{key.upper()}")
            current_val = getattr(self, key)
            default_val = self.__class__.model_fields[key].default
            if legacy_val is not None and current_val == default_val:
                try:
                    field_type = self.__class__.model_fields[key].annotation
                    setattr(self, key, field_type(legacy_val))
                except Exception:
                    setattr(self, key, legacy_val)

settings = Settings()
