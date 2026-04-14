from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()


class AppSettings(BaseModel):
    app_name: str = "Verwaltung Radsport Koch GmbH"
    environment: str = Field(default="development")
    database_url: str = Field(default="sqlite:///data/radsport_koch.db")
    log_level: str = Field(default="INFO")
    company_name: str = "Radsport Koch GmbH"
    data_directory: Path = Path("data")
    export_directory: Path = Path("exports")
    enable_seed_on_first_run: bool = True

    @property
    def database_url_for_sqlalchemy(self) -> str:
        if self.database_url.startswith("sqlite:///"):
            database_path = self.database_url.removeprefix("sqlite:///")
            return f"sqlite:///{Path(database_path).as_posix()}"
        return self.database_url


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    # Die Konfiguration wird bewusst zentral geladen, damit Datenbank,
    # Logging und Exportpfade in allen Schichten konsistent bleiben.
    return AppSettings(
        environment=os.getenv("APP_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///data/radsport_koch.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        enable_seed_on_first_run=os.getenv("ENABLE_SEED_ON_FIRST_RUN", "true").lower() == "true",
    )
