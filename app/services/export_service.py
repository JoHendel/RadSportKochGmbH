from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.utils.csv_export import export_rows_to_csv


class ExportService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def export(self, filename: str, headers: list[str], rows: list[list[object]]) -> Path:
        export_path = (self.settings.export_directory / filename).resolve()
        export_path.parent.mkdir(parents=True, exist_ok=True)
        return export_rows_to_csv(export_path, headers, rows)
