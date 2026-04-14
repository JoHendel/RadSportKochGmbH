from __future__ import annotations

from app.core.enums import OrderStatus, PaymentStatus


def order_status_label(status: OrderStatus) -> str:
    labels = {
        OrderStatus.DRAFT: "Entwurf",
        OrderStatus.OPEN: "Offen",
        OrderStatus.PROCESSING: "In Bearbeitung",
        OrderStatus.COMPLETED: "Abgeschlossen",
        OrderStatus.CANCELLED: "Storniert",
    }
    return labels[status]


def payment_status_label(status: PaymentStatus) -> str:
    labels = {
        PaymentStatus.PENDING: "Offen",
        PaymentStatus.PARTIALLY_PAID: "Teilweise bezahlt",
        PaymentStatus.PAID: "Bezahlt",
        PaymentStatus.REFUNDED: "Erstattet",
    }
    return labels[status]


def status_color(value: str) -> str:
    mapping = {
        "draft": "#7f8c8d",
        "open": "#e67e22",
        "processing": "#2980b9",
        "completed": "#27ae60",
        "cancelled": "#c0392b",
        "pending": "#d35400",
        "partially_paid": "#8e44ad",
        "paid": "#27ae60",
        "refunded": "#7f8c8d",
    }
    return mapping.get(value, "#34495e")
