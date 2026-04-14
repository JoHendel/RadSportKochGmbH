from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout


class DetailCard(QFrame):
    def __init__(self, title: str) -> None:
        super().__init__()
        self.setProperty("panel", True)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(22, 22, 22, 22)
        root_layout.setSpacing(16)

        title_label = QLabel(title)
        title_label.setProperty("role", "sectionTitle")
        root_layout.addWidget(title_label)

        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(12)
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignTop)
        root_layout.addLayout(self.form_layout)

    def set_rows(self, rows: list[tuple[str, str]]) -> None:
        while self.form_layout.rowCount():
            self.form_layout.removeRow(0)
        for label, value in rows:
            label_widget = QLabel(label)
            label_widget.setStyleSheet("font-size: 12px; color: #6b7b88; font-weight: 700;")
            value_widget = QLabel(value)
            value_widget.setWordWrap(True)
            value_widget.setStyleSheet("font-size: 13px; color: #21313c;")
            self.form_layout.addRow(label_widget, value_widget)
