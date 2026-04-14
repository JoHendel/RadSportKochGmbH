from __future__ import annotations

from datetime import date

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from app.core.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem


class OrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list(
        self,
        search: str = "",
        customer_id: int | None = None,
        status: OrderStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Order]:
        statement = (
            select(Order)
            .options(joinedload(Order.customer), joinedload(Order.items).joinedload(OrderItem.product))
            .order_by(Order.order_date.desc(), Order.id.desc())
        )

        filters = []
        if search:
            pattern = f"%{search.strip()}%"
            filters.append(Order.order_number.ilike(pattern))
        if customer_id is not None:
            filters.append(Order.customer_id == customer_id)
        if status is not None:
            filters.append(Order.status == status)
        if start_date is not None:
            filters.append(Order.order_date >= start_date)
        if end_date is not None:
            filters.append(Order.order_date <= end_date)
        if filters:
            statement = statement.where(and_(*filters))

        return list(self.session.scalars(statement).unique().all())

    def recent(self, limit: int = 8) -> list[Order]:
        statement = (
            select(Order)
            .options(joinedload(Order.customer))
            .order_by(Order.order_date.desc(), Order.id.desc())
            .limit(limit)
        )
        return list(self.session.scalars(statement).unique().all())

    def get(self, order_id: int) -> Order | None:
        statement = (
            select(Order)
            .options(joinedload(Order.customer), joinedload(Order.items).joinedload(OrderItem.product))
            .where(Order.id == order_id)
        )
        return self.session.scalars(statement).unique().first()

    def add(self, order: Order) -> Order:
        self.session.add(order)
        self.session.flush()
        return order

    def delete(self, order: Order) -> None:
        self.session.delete(order)
