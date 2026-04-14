from __future__ import annotations


def build_stylesheet() -> str:
    # Das zentrale Stylesheet bündelt die visuelle Sprache der Anwendung,
    # damit einzelne Views nicht mit verstreuten Inline-Stilen gepflegt werden.
    return """
    QWidget {
        background-color: #f3efe7;
        color: #21313c;
        font-family: "SF Pro Text", "Segoe UI", "Helvetica Neue", sans-serif;
        font-size: 13px;
    }

    QMainWindow, QStackedWidget, QSplitter, QSplitter > QWidget {
        background-color: #f3efe7;
    }

    QToolBar {
        background: #fbf8f2;
        border: none;
        border-bottom: 1px solid #dfd6c7;
        spacing: 12px;
        padding: 12px 16px;
    }

    QToolButton {
        background: #ece4d7;
        border: 1px solid #d7ccba;
        border-radius: 13px;
        padding: 9px 15px;
        font-weight: 600;
        color: #29414f;
    }

    QToolButton:hover {
        background: #e3d8c9;
    }

    QPushButton {
        background-color: #1b6c61;
        color: white;
        border: none;
        border-radius: 13px;
        padding: 10px 16px;
        font-weight: 700;
    }

    QPushButton:hover {
        background-color: #16584f;
    }

    QPushButton:pressed {
        background-color: #124740;
    }

    QPushButton[variant="secondary"] {
        background-color: #ece4d7;
        color: #29414f;
        border: 1px solid #d7ccba;
    }

    QPushButton[variant="secondary"]:hover {
        background-color: #e1d6c7;
    }

    QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
        background: #fffdf9;
        border: 1px solid #d8d0c2;
        border-radius: 14px;
        padding: 9px 12px;
        selection-background-color: #1f6f5f;
    }

    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {
        border: 1px solid #1f6f5f;
    }

    QListWidget#NavigationList {
        background: transparent;
        border: none;
        outline: none;
        padding: 6px 0;
    }

    QListWidget#NavigationList::item {
        background: transparent;
        border-radius: 14px;
        padding: 14px 16px;
        margin: 4px 8px;
        color: #4b5563;
        font-size: 14px;
        font-weight: 600;
    }

    QListWidget#NavigationList::item:selected {
        background: #1f6f5f;
        color: white;
    }

    QListWidget#NavigationList::item:hover:!selected {
        background: #efe7da;
    }

    QHeaderView::section {
        background: #f7f2e8;
        color: #516170;
        border: none;
        border-bottom: 1px solid #e3dccf;
        padding: 10px 12px;
        font-size: 12px;
        font-weight: 700;
    }

    QTableWidget {
        background: #fffdf9;
        border: 1px solid #e1dacf;
        border-radius: 18px;
        gridline-color: #efe7da;
        alternate-background-color: #fcfaf6;
        selection-background-color: #d9ece7;
        selection-color: #163630;
        padding: 6px;
    }

    QListWidget {
        background: #fffdf9;
        border: 1px solid #e1dacf;
        border-radius: 18px;
        padding: 8px;
    }

    QListWidget::item {
        border-radius: 12px;
        padding: 10px 12px;
        margin: 4px 2px;
    }

    QListWidget::item:selected {
        background: #d9ece7;
        color: #173630;
    }

    QScrollBar:vertical {
        background: transparent;
        width: 12px;
        margin: 10px 2px 10px 0;
    }

    QScrollBar::handle:vertical {
        background: #cfc5b6;
        border-radius: 6px;
        min-height: 30px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical,
    QScrollBar:horizontal, QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal,
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        border: none;
        background: transparent;
        height: 0px;
        width: 0px;
    }

    QLabel[role="pageTitle"] {
        font-size: 30px;
        font-weight: 800;
        color: #1f2933;
    }

    QLabel[role="pageSubtitle"] {
        color: #667085;
        font-size: 13px;
    }

    QLabel[role="sectionTitle"] {
        font-size: 18px;
        font-weight: 800;
        color: #233744;
    }

    QFrame[panel="true"] {
        background: #fffdf9;
        border: 1px solid #e1dacf;
        border-radius: 22px;
    }
    """
