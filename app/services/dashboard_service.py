from __future__ import annotations

from sqlalchemy.orm import Session

from app.repositories.dashboard_repository import DashboardRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.dashboard import DashboardMetrics


class DashboardService:
    def __init__(self, session: Session) -> None:
        self.dashboard_repository = DashboardRepository(session)
        self.order_repository = OrderRepository(session)
        self.product_repository = ProductRepository(session)

    def get_metrics(self) -> DashboardMetrics:
        return self.dashboard_repository.get_metrics()

    def get_recent_orders(self):
        return self.order_repository.recent(limit=8)

    def get_low_stock_products(self):
        return self.product_repository.low_stock()
