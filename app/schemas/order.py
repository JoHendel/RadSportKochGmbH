from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.core.enums import OrderStatus, PaymentStatus


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)
    unit_price: Decimal = Field(gt=Decimal("0"))


class OrderBaseSchema(BaseModel):
    order_number: str = Field(min_length=3, max_length=30)
    customer_id: int
    order_date: date
    status: OrderStatus
    payment_status: PaymentStatus
    notes: str | None = None
    items: list[OrderItemSchema] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_items(self) -> "OrderBaseSchema":
        # Eine Bestellung ohne Positionen wäre fachlich wertlos und würde
        # in der Summenberechnung zu widersprüchlichem Verhalten führen.
        if not self.items:
            raise ValueError("Mindestens eine Bestellposition ist erforderlich.")
        return self


class OrderCreateSchema(OrderBaseSchema):
    pass


class OrderUpdateSchema(OrderBaseSchema):
    pass


class OrderReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_number: str
    customer_id: int
    order_date: date
    status: OrderStatus
    payment_status: PaymentStatus
    notes: str | None
    total_amount: Decimal
    created_at: datetime
