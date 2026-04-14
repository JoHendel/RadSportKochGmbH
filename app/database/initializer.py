from __future__ import annotations

from pathlib import Path

from app.core.config import get_settings
from app.database.base import Base
from app.database.session import engine, session_scope
from app.models import Customer, Order, OrderItem, Product
from app.services.seed_service import SeedService


def initialize_database() -> None:
    settings = get_settings()
    settings.data_directory.mkdir(parents=True, exist_ok=True)
    settings.export_directory.mkdir(parents=True, exist_ok=True)

    # Die Tabellen werden für den Erststart automatisch angelegt.
    # Alembic bleibt zusätzlich vorbereitet, damit spätere Schemaänderungen
    # sauber migriert werden können.
    Base.metadata.create_all(bind=engine)

    if settings.enable_seed_on_first_run:
        with session_scope() as session:
            has_customers = session.query(Customer).first() is not None
            has_products = session.query(Product).first() is not None
            has_orders = session.query(Order).first() is not None
            has_items = session.query(OrderItem).first() is not None
            if not any([has_customers, has_products, has_orders, has_items]):
                SeedService(session).seed()
