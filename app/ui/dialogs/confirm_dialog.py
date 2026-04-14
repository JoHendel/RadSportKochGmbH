from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget


def ask_delete_confirmation(parent: QWidget, entity_name: str) -> bool:
    result = QMessageBox.question(
        parent,
        "Löschen bestätigen",
        f"Soll '{entity_name}' wirklich gelöscht werden?",
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No,
    )
    return result == QMessageBox.StandardButton.Yes
