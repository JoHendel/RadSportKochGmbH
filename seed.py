from __future__ import annotations

from app.core.logging_config import configure_logging
from app.database.base import Base
from app.database.session import engine, session_scope
from app.services.seed_service import SeedService


def main() -> None:
    configure_logging()
    Base.metadata.create_all(bind=engine)
    with session_scope() as session:
        SeedService(session).seed()


if __name__ == "__main__":
    main()
