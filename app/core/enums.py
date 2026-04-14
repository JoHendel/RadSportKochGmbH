from __future__ import annotations

from enum import StrEnum


class ProductCategory(StrEnum):
    BICYCLE = "Bicycle"
    SPARE_PART = "Spare Part"
    ACCESSORY = "Accessory"
    CLOTHING = "Clothing"


class OrderStatus(StrEnum):
    DRAFT = "draft"
    OPEN = "open"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    REFUNDED = "refunded"
