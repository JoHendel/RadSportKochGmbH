from __future__ import annotations

from datetime import datetime

from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QSplitter, QTableWidgetItem, QVBoxLayout, QWidget
from qfluentwidgets import ComboBox, PrimaryPushButton, PushButton

from app.core.enums import OrderStatus
from app.database.session import session_scope
from app.services.customer_service import CustomerService
from app.services.exceptions import BusinessRuleError, EntityNotFoundError, ValidationServiceError
from app.services.export_service import ExportService
from app.services.order_service import OrderService
from app.services.product_service import ProductService
from app.ui.dialogs.confirm_dialog import ask_delete_confirmation
from app.ui.dialogs.order_dialog import OrderDialog
from app.ui.views.order_detail_view import OrderDetailView
from app.ui.widgets.filter_bar import FilterBar
from app.ui.widgets.table_widget import DataTableWidget
from app.utils.formatters import format_currency, format_date
from app.utils.status_helpers import order_status_label, payment_status_label


class OrdersView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.orders = []
        self.customers = []

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        title = QLabel("Bestellverwaltung")
        title.setProperty("role", "pageTitle")
        subtitle = QLabel("Verfolge Aufträge, Zahlstatus und Positionen in einer kompakten Operativansicht.")
        subtitle.setProperty("role", "pageSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        actions_layout = QHBoxLayout()
        self.filter_bar = FilterBar("Bestellungen suchen...")
        self.filter_bar.search_input.textChanged.connect(self.refresh_data)

        self.customer_filter = ComboBox()
        self.customer_filter.currentIndexChanged.connect(self.refresh_data)
        self.filter_bar.add_labeled_widget("Kunde", self.customer_filter)

        self.status_filter = ComboBox()
        self.status_filter.addItem("Alle Status", None)
        for status in OrderStatus:
            self.status_filter.addItem(order_status_label(status), status)
        self.status_filter.currentIndexChanged.connect(self.refresh_data)
        self.filter_bar.add_labeled_widget("Status", self.status_filter)

        actions_layout.addWidget(self.filter_bar, 1)

        add_button = PrimaryPushButton("Bestellung anlegen")
        add_button.clicked.connect(self.create_order)
        edit_button = PushButton("Bearbeiten")
        edit_button.clicked.connect(self.edit_order)
        delete_button = PushButton("Löschen")
        delete_button.clicked.connect(self.delete_order)
        export_button = PushButton("CSV exportieren")
        export_button.clicked.connect(self.export_csv)

        for button in [add_button, edit_button, delete_button, export_button]:
            actions_layout.addWidget(button)
        root_layout.addLayout(actions_layout)

        splitter = QSplitter()
        self.table = DataTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["Nr.", "Kunde", "Datum", "Status", "Zahlstatus", "Gesamt", "Positionen"]
        )
        self.table.itemSelectionChanged.connect(self._handle_selection_changed)
        splitter.addWidget(self.table)

        self.detail_view = OrderDetailView()
        splitter.addWidget(self.detail_view)
        splitter.setSizes([980, 460])
        root_layout.addWidget(splitter, 1)

        self._load_customers()

    def _load_customers(self) -> None:
        with session_scope() as session:
            self.customers = CustomerService(session).list_customers()
        self.customer_filter.blockSignals(True)
        self.customer_filter.clear()
        self.customer_filter.addItem("Alle Kunden", None)
        for customer in self.customers:
            self.customer_filter.addItem(customer.full_name, customer.id)
        self.customer_filter.blockSignals(False)

    def refresh_data(self) -> None:
        self._load_customers()
        with session_scope() as session:
            service = OrderService(session)
            self.orders = service.list_orders(
                search=self.filter_bar.search_input.text(),
                customer_id=self.customer_filter.currentData(),
                status=self.status_filter.currentData(),
            )

        self.table.setRowCount(len(self.orders))
        for row, order in enumerate(self.orders):
            self.table.setItem(row, 0, QTableWidgetItem(order.order_number))
            self.table.setItem(row, 1, QTableWidgetItem(order.customer.full_name))
            self.table.setItem(row, 2, QTableWidgetItem(format_date(order.order_date)))
            self.table.setItem(row, 3, QTableWidgetItem(order_status_label(order.status)))
            self.table.setItem(row, 4, QTableWidgetItem(payment_status_label(order.payment_status)))
            self.table.setItem(row, 5, QTableWidgetItem(format_currency(order.total_amount)))
            self.table.setItem(row, 6, QTableWidgetItem(str(len(order.items))))
        self.detail_view.set_order(None)
        if self.orders:
            self.table.selectRow(0)

    def _current_order(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.orders):
            return None
        return self.orders[row]

    def _handle_selection_changed(self) -> None:
        order = self._current_order()
        if not order:
            self.detail_view.set_order(None)
            return
        with session_scope() as session:
            full_order = OrderService(session).get_order(order.id)
        self.detail_view.set_order(full_order)

    def create_order(self) -> None:
        with session_scope() as session:
            customers = CustomerService(session).list_customers()
            products = ProductService(session).list_products()
        dialog = OrderDialog(customers=customers, products=products, parent=self)
        if dialog.exec():
            try:
                with session_scope() as session:
                    OrderService(session).create_order(dialog.get_data())
                self.refresh_data()
            except (ValidationServiceError, BusinessRuleError) as exc:
                QMessageBox.warning(self, "Fehler", str(exc))

    def edit_order(self) -> None:
        order = self._current_order()
        if not order:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst eine Bestellung auswählen.")
            return
        with session_scope() as session:
            customers = CustomerService(session).list_customers()
            products = ProductService(session).list_products()
            full_order = OrderService(session).get_order(order.id)
        dialog = OrderDialog(customers=customers, products=products, parent=self, order=full_order)
        if dialog.exec():
            try:
                with session_scope() as session:
                    OrderService(session).update_order(order.id, dialog.get_data())
                self.refresh_data()
            except (ValidationServiceError, BusinessRuleError, EntityNotFoundError) as exc:
                QMessageBox.warning(self, "Fehler", str(exc))

    def delete_order(self) -> None:
        order = self._current_order()
        if not order:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst eine Bestellung auswählen.")
            return
        if not ask_delete_confirmation(self, order.order_number):
            return
        try:
            with session_scope() as session:
                OrderService(session).delete_order(order.id)
            self.refresh_data()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"Bestellung konnte nicht gelöscht werden:\n{exc}")

    def export_csv(self) -> None:
        rows = [
            [
                order.order_number,
                order.customer.full_name,
                order.order_date.isoformat(),
                order_status_label(order.status),
                payment_status_label(order.payment_status),
                f"{order.total_amount:.2f}",
                len(order.items),
            ]
            for order in self.orders
        ]
        path = ExportService().export(
            filename=f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            headers=["Bestellnummer", "Kunde", "Datum", "Status", "Zahlstatus", "Gesamtbetrag", "Positionen"],
            rows=rows,
        )
        QMessageBox.information(self, "Export erfolgreich", f"CSV-Datei wurde erstellt:\n{path}")
