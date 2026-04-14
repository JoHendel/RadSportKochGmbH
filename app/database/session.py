from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


settings = get_settings()

connect_args: dict[str, object] = {}
if settings.database_url_for_sqlalchemy.startswith("sqlite:///"):
    # SQLite benötigt diese Option für den Zugriff aus einer Desktop-Anwendung,
    # in der mehrere Qt-Signale denselben Prozesskontext nutzen.
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.database_url_for_sqlalchemy,
    echo=False,
    future=True,
    connect_args=connect_args,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, class_=Session)


@contextmanager
def session_scope() -> Session:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
