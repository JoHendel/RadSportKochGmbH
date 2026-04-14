from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import OrderStatus, PaymentStatus
from app.database.base import Base
from app.models.mixins import TimestampMixin


class Order(TimestampMixin, Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_number: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False, index=True)
    order_date: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default=OrderStatus.OPEN)
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        nullable=False,
        default=PaymentStatus.PENDING,
    )
    notes: Mapped[str | None] = mapped_column(Text)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False, default=0)

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def recalculate_total(self) -> Decimal:
        # Die Bestellsumme wird ausschließlich aus den Positionen berechnet,
        # damit keine manuell gepflegten Summen von der Realität abweichen.
        total = sum((item.total_price for item in self.items), start=Decimal("0.00"))
        self.total_amount = total.quantize(Decimal("0.01"))
        return self.total_amount
