from __future__ import annotations

from datetime import date
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.enums import OrderStatus
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.schemas.dashboard import DashboardMetrics


class DashboardRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_metrics(self) -> DashboardMetrics:
        today = date.today()
        month_start = today.replace(day=1)
        year_start = today.replace(month=1, day=1)

        total_customers = self.session.scalar(select(func.count(Customer.id))) or 0
        total_products = self.session.scalar(select(func.count(Product.id))) or 0
        open_orders = self.session.scalar(
            select(func.count(Order.id)).where(Order.status.in_([OrderStatus.OPEN, OrderStatus.PROCESSING]))
        ) or 0
        low_stock_products = self.session.scalar(
            select(func.count(Product.id)).where(Product.stock_quantity <= Product.minimum_stock)
        ) or 0
        monthly_revenue = self.session.scalar(
            select(func.coalesce(func.sum(Order.total_amount), 0)).where(
                Order.order_date >= month_start,
                Order.status != OrderStatus.CANCELLED,
            )
        ) or Decimal("0.00")
        current_year_revenue = self.session.scalar(
            select(func.coalesce(func.sum(Order.total_amount), 0)).where(
                Order.order_date >= year_start,
                Order.status != OrderStatus.CANCELLED,
            )
        ) or Decimal("0.00")

        return DashboardMetrics(
            total_customers=total_customers,
            total_products=total_products,
            open_orders=open_orders,
            low_stock_products=low_stock_products,
            monthly_revenue=Decimal(monthly_revenue),
            current_year_revenue=Decimal(current_year_revenue),
        )
