from __future__ import annotations

import csv
from pathlib import Path


def export_rows_to_csv(path: Path, headers: list[str], rows: list[list[object]]) -> Path:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(headers)
        writer.writerows(rows)
    return path
