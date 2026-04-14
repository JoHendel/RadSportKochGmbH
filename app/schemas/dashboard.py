from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class DashboardMetrics:
    total_customers: int
    total_products: int
    open_orders: int
    low_stock_products: int
    monthly_revenue: Decimal
    current_year_revenue: Decimal
