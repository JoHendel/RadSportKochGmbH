from __future__ import annotations

import sys

from app.core.logging_config import configure_logging
from app.database.initializer import initialize_database
from app.ui.application import create_application
from app.ui.main_window import MainWindow


def main() -> int:
    configure_logging()
    initialize_database()
    app = create_application()
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
