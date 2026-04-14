from __future__ import annotations

from datetime import date
from decimal import Decimal

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.enums import OrderStatus
from app.models.order import Order
from app.models.order_item import OrderItem
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreateSchema, OrderUpdateSchema
from app.services.exceptions import BusinessRuleError, EntityNotFoundError, ValidationServiceError


class OrderService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = OrderRepository(session)
        self.customer_repository = CustomerRepository(session)
        self.product_repository = ProductRepository(session)

    def list_orders(
        self,
        search: str = "",
        customer_id: int | None = None,
        status: OrderStatus | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[Order]:
        return self.repository.list(search=search, customer_id=customer_id, status=status, start_date=start_date, end_date=end_date)

    def recent_orders(self, limit: int = 8) -> list[Order]:
        return self.repository.recent(limit=limit)

    def get_order(self, order_id: int) -> Order:
        order = self.repository.get(order_id)
        if not order:
            raise EntityNotFoundError("Bestellung wurde nicht gefunden.")
        return order

    def create_order(self, data: dict) -> Order:
        try:
            payload = OrderCreateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        return self._save_order(order=None, payload=payload)

    def update_order(self, order_id: int, data: dict) -> Order:
        order = self.get_order(order_id)
        try:
            payload = OrderUpdateSchema(**data)
        except ValidationError as exc:
            raise ValidationServiceError("\n".join(error["msg"] for error in exc.errors())) from exc

        return self._save_order(order=order, payload=payload)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)
        self._restore_stock(order)
        self.repository.delete(order)

    def _save_order(self, order: Order | None, payload: OrderCreateSchema | OrderUpdateSchema) -> Order:
        customer = self.customer_repository.get(payload.customer_id)
        if not customer:
            raise ValidationServiceError("Gewählter Kunde ist nicht vorhanden.")

        if order is None:
            order = Order(
                order_number=payload.order_number,
                customer_id=payload.customer_id,
                order_date=payload.order_date,
                status=payload.status,
                payment_status=payload.payment_status,
                notes=payload.notes,
            )
            self.repository.add(order)
        else:
            # Vor dem Neuberechnen werden alte Lagerbewegungen rückgängig gemacht,
            # damit nach einer Änderung immer exakt der finale Stand erhalten bleibt.
            self._restore_stock(order)
            order.order_number = payload.order_number
            order.customer_id = payload.customer_id
            order.order_date = payload.order_date
            order.status = payload.status
            order.payment_status = payload.payment_status
            order.notes = payload.notes
            order.items.clear()
            self.session.flush()

        items: list[OrderItem] = []
        for item_data in payload.items:
            product = self.product_repository.get(item_data.product_id)
            if not product:
                raise ValidationServiceError("Mindestens ein gewählter Artikel ist nicht vorhanden.")
            if payload.status != OrderStatus.CANCELLED and product.stock_quantity < item_data.quantity:
                raise BusinessRuleError(f"Lagerbestand für '{product.name}' ist zu niedrig.")

            order_item = OrderItem(
                product_id=product.id,
                quantity=item_data.quantity,
                unit_price=Decimal(item_data.unit_price),
                total_price=Decimal("0.00"),
            )
            order_item.recalculate_total()
            items.append(order_item)
            order.items.append(order_item)

            if payload.status != OrderStatus.CANCELLED:
                product.stock_quantity -= item_data.quantity

        order.recalculate_total()
        self.session.flush()
        return order

    def _restore_stock(self, order: Order) -> None:
        # Beim Löschen oder Bearbeiten einer Bestellung werden die früher
        # abgezogenen Bestände zurückgeführt, sofern die Bestellung nicht
        # bereits storniert war.
        if order.status == OrderStatus.CANCELLED:
            return
        for item in order.items:
            product = self.product_repository.get(item.product_id)
            if product:
                product.stock_quantity += item.quantity
