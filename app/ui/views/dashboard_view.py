from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QVBoxLayout, QWidget

from app.database.session import session_scope
from app.services.dashboard_service import DashboardService
from app.ui.widgets.card_widget import MetricCard
from app.utils.formatters import format_currency, format_date
from app.utils.status_helpers import order_status_label


class DashboardView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(18)

        title = QLabel("Dashboard")
        title.setProperty("role", "pageTitle")
        subtitle = QLabel("Kennzahlen, Umsatzentwicklung und aktuelle Vorgänge für den Tagesbetrieb.")
        subtitle.setProperty("role", "pageSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(16)
        self.customer_card = MetricCard("Kunden", "0", "#1d4ed8", "#eaf2ff")
        self.product_card = MetricCard("Artikel", "0", "#0f766e", "#eaf8f4")
        self.open_order_card = MetricCard("Offene Bestellungen", "0", "#ea580c", "#fff1e8")
        self.low_stock_card = MetricCard("Niedrige Lagerbestände", "0", "#b91c1c", "#fdecec")
        cards_layout.addWidget(self.customer_card, 0, 0)
        cards_layout.addWidget(self.product_card, 0, 1)
        cards_layout.addWidget(self.open_order_card, 0, 2)
        cards_layout.addWidget(self.low_stock_card, 0, 3)
        root_layout.addLayout(cards_layout)

        revenue_layout = QHBoxLayout()
        self.monthly_revenue_card = MetricCard("Umsatz aktueller Monat", "0,00 EUR", "#7c3aed", "#f5edff")
        self.year_revenue_card = MetricCard("Umsatz aktuelles Jahr", "0,00 EUR", "#0369a1", "#eaf6ff")
        revenue_layout.addWidget(self.monthly_revenue_card)
        revenue_layout.addWidget(self.year_revenue_card)
        root_layout.addLayout(revenue_layout)

        lists_layout = QHBoxLayout()
        self.recent_orders_list = QListWidget()
        self.recent_orders_list.setSpacing(6)
        self.low_stock_list = QListWidget()
        self.low_stock_list.setSpacing(6)
        lists_layout.addWidget(self._with_title("Aktuelle Bestellungen", self.recent_orders_list), 2)
        lists_layout.addWidget(self._with_title("Lagerwarnungen", self.low_stock_list), 1)
        root_layout.addLayout(lists_layout, 1)

    def _with_title(self, title: str, widget: QWidget) -> QWidget:
        container = QFrame()
        container.setProperty("panel", True)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(18, 18, 18, 18)
        label = QLabel(title)
        label.setProperty("role", "sectionTitle")
        layout.addWidget(label)
        layout.addWidget(widget)
        return container

    def refresh_data(self) -> None:
        with session_scope() as session:
            service = DashboardService(session)
            metrics = service.get_metrics()
            recent_orders = service.get_recent_orders()
            low_stock_products = service.get_low_stock_products()

        self.customer_card.update_value(str(metrics.total_customers))
        self.product_card.update_value(str(metrics.total_products))
        self.open_order_card.update_value(str(metrics.open_orders))
        self.low_stock_card.update_value(str(metrics.low_stock_products))
        self.monthly_revenue_card.update_value(format_currency(metrics.monthly_revenue))
        self.year_revenue_card.update_value(format_currency(metrics.current_year_revenue))

        self.recent_orders_list.clear()
        for order in recent_orders:
            item_widget = self._create_dashboard_list_item(
                title=f"{order.order_number} - {order.customer.full_name}",
                subtitle=(
                    f"Status: {order_status_label(order.status)}\n"
                    f"Datum: {format_date(order.order_date)}\n"
                    f"Gesamtbetrag: {format_currency(order.total_amount)}"
                ),
            )
            item = QListWidgetItem(self.recent_orders_list)
            item.setSizeHint(item_widget.sizeHint())
            self.recent_orders_list.addItem(item)
            self.recent_orders_list.setItemWidget(item, item_widget)

        self.low_stock_list.clear()
        for product in low_stock_products:
            item_widget = self._create_dashboard_list_item(
                title=product.name,
                subtitle=f"Bestand: {product.stock_quantity}\nMindestbestand: {product.minimum_stock}",
            )
            item = QListWidgetItem(self.low_stock_list)
            item.setSizeHint(item_widget.sizeHint())
            self.low_stock_list.addItem(item)
            self.low_stock_list.setItemWidget(item, item_widget)

    def _create_dashboard_list_item(self, title: str, subtitle: str) -> QWidget:
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; font-weight: 700; color: #21313c;")
        title_label.setWordWrap(True)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        subtitle_label.setStyleSheet("font-size: 12px; color: #617280; line-height: 1.45;")
        subtitle_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        return container
