from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class MetricCard(QFrame):
    def __init__(self, title: str, value: str, accent_color: str, background_color: str | None = None) -> None:
        super().__init__()
        self.setProperty("panel", True)
        bg = background_color or "#ffffff"
        self.setStyleSheet(
            f"""
            QFrame[panel="true"] {{
                border-left: 6px solid {accent_color};
                background: {bg};
                border: 1px solid rgba(31, 49, 60, 0.08);
                border-radius: 18px;
            }}
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(6)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet("font-size: 12px; color: #4f6270; font-weight: 700; text-transform: uppercase;")
        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"font-size: 30px; font-weight: 800; color: {accent_color};")
        self.caption_label = QLabel("Aktueller Stand")
        self.caption_label.setStyleSheet("font-size: 12px; color: #6f808d;")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.caption_label)

    def update_value(self, value: str) -> None:
        self.value_label.setText(value)
