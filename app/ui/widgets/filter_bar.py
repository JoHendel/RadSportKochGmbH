from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget
from qfluentwidgets import SearchLineEdit


class FilterBar(QWidget):
    def __init__(self, placeholder: str) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.search_input = SearchLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.setClearButtonEnabled(True)
        layout.addWidget(self.search_input, 1)

        self.extra_widgets: list[QWidget] = []

    def add_labeled_widget(self, label: str, widget: QWidget) -> None:
        row = QHBoxLayout()
        row.setSpacing(6)
        row.addWidget(QLabel(label))
        row.addWidget(widget)
        container = QWidget()
        container.setLayout(row)
        self.layout().addWidget(container)
        self.extra_widgets.append(container)
