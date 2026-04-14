from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMainWindow, QStackedWidget, QVBoxLayout, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import NavigationInterface, NavigationItemPosition

from app.ui.views.customers_view import CustomersView
from app.ui.views.dashboard_view import DashboardView
from app.ui.views.orders_view import OrdersView
from app.ui.views.products_view import ProductsView


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Verwaltung Radsport Koch GmbH")
        self.resize(1440, 920)

        self.dashboard_view = DashboardView()
        self.customers_view = CustomersView()
        self.products_view = ProductsView()
        self.orders_view = OrdersView()

        self.navigation = NavigationInterface(self, showMenuButton=True, collapsible=True)
        self.navigation.setMinimumWidth(68)
        self.navigation.setExpandWidth(250)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.dashboard_view)
        self.stack.addWidget(self.customers_view)
        self.stack.addWidget(self.products_view)
        self.stack.addWidget(self.orders_view)

        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(20, 16, 20, 20)
        content_layout.setSpacing(12)

        header = QLabel("Verwaltung Radsport Koch GmbH")
        header.setStyleSheet("font-size: 28px; font-weight: 700; padding: 8px 4px;")
        subheader = QLabel("Modernes Verwaltungscockpit fuer Verkauf, Kunden, Lager und Bestellungen")
        subheader.setStyleSheet("font-size: 13px; color: grey; padding: 0 4px 8px 4px;")
        content_layout.addWidget(header)
        content_layout.addWidget(subheader)
        content_layout.addWidget(self.stack, 1)

        root = QWidget()
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(self.navigation)
        root_layout.addWidget(content_wrapper, 1)
        self.setCentralWidget(root)

        self._init_navigation()
        self.refresh_all()

    def _init_navigation(self) -> None:
        self.navigation.addItem("dashboard", FIF.HOME, "Dashboard", onClick=lambda: self._switch_to(0))
        self.navigation.addItem("customers", FIF.PEOPLE, "Kunden", onClick=lambda: self._switch_to(1))
        self.navigation.addItem("products", FIF.TAG, "Artikel", onClick=lambda: self._switch_to(2))
        self.navigation.addItem("orders", FIF.SHOPPING_CART, "Bestellungen", onClick=lambda: self._switch_to(3))
        self.navigation.addSeparator()
        self.navigation.addItem(
            routeKey="refresh",
            icon=FIF.SYNC,
            text="Aktualisieren",
            onClick=self.refresh_all,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )
        self.navigation.setCurrentItem("dashboard")

    def _switch_to(self, index: int) -> None:
        self.stack.setCurrentIndex(index)

    def refresh_all(self) -> None:
        self.dashboard_view.refresh_data()
        self.customers_view.refresh_data()
        self.products_view.refresh_data()
        self.orders_view.refresh_data()
