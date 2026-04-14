from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import Theme, setTheme, setThemeColor


def create_application() -> QApplication:
    app = QApplication(sys.argv)
    app.setApplicationName("Verwaltung Radsport Koch GmbH")
    app.setOrganizationName("Radsport Koch GmbH")
    # Das Fluent-Theme übernimmt bewusst die visuelle Hauptsprache der App,
    # damit Navigation, Eingaben und Tabellen konsistent modern erscheinen.
    setTheme(Theme.LIGHT)
    setThemeColor("#1b6c61")
    return app
