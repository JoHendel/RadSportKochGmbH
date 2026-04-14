from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel

from app.utils.status_helpers import status_color


class StatusBadge(QLabel):
    def __init__(self, text: str, value_key: str) -> None:
        super().__init__(text)
        color = status_color(value_key)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 4px 10px;
                font-weight: 600;
            }}
            """
        )
