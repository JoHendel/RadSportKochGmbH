from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.enums import OrderStatus, PaymentStatus, ProductCategory
from app.database.base import Base
from app.models.customer import Customer
from app.models.product import Product
from app.services.order_service import OrderService


def test_order_creation_reduces_stock_and_calculates_total():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

    with session_factory() as session:
        customer = Customer(customer_number="C-1", first_name="Max", last_name="Muster")
        product = Product(
            article_number="P-1",
            name="Test Bike",
            category=ProductCategory.BICYCLE,
            purchase_price=Decimal("100.00"),
            sale_price=Decimal("150.00"),
            stock_quantity=5,
            minimum_stock=1,
            is_active=True,
        )
        session.add_all([customer, product])
        session.commit()

        service = OrderService(session)
        order = service.create_order(
            {
                "order_number": "O-1",
                "customer_id": customer.id,
                "order_date": date.today(),
                "status": OrderStatus.OPEN,
                "payment_status": PaymentStatus.PENDING,
                "notes": "Test",
                "items": [{"product_id": product.id, "quantity": 2, "unit_price": "150.00"}],
            }
        )
        session.commit()

        assert order.total_amount == Decimal("300.00")
        assert session.get(Product, product.id).stock_quantity == 3
