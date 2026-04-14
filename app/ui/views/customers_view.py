from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QSplitter, QTableWidgetItem, QVBoxLayout, QWidget
from qfluentwidgets import PrimaryPushButton, PushButton

from app.database.session import session_scope
from app.services.customer_service import CustomerService
from app.services.exceptions import EntityNotFoundError, ValidationServiceError
from app.services.export_service import ExportService
from app.ui.dialogs.confirm_dialog import ask_delete_confirmation
from app.ui.dialogs.customer_dialog import CustomerDialog
from app.ui.views.customer_detail_view import CustomerDetailView
from app.ui.widgets.filter_bar import FilterBar
from app.ui.widgets.table_widget import DataTableWidget
from app.utils.formatters import format_date


class CustomersView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.customers = []
        self.selected_customer_id: int | None = None

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        title = QLabel("Kundenverwaltung")
        title.setProperty("role", "pageTitle")
        subtitle = QLabel("Verwalte Stammkunden, Kontaktdaten und Bestellhistorien zentral an einem Ort.")
        subtitle.setProperty("role", "pageSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        actions_layout = QHBoxLayout()
        self.filter_bar = FilterBar("Kunden suchen...")
        self.filter_bar.search_input.textChanged.connect(self.refresh_data)
        actions_layout.addWidget(self.filter_bar, 1)

        add_button = PrimaryPushButton("Kunde anlegen")
        add_button.clicked.connect(self.create_customer)
        edit_button = PushButton("Bearbeiten")
        edit_button.clicked.connect(self.edit_customer)
        delete_button = PushButton("Löschen")
        delete_button.clicked.connect(self.delete_customer)
        export_button = PushButton("CSV exportieren")
        export_button.clicked.connect(self.export_csv)

        for button in [add_button, edit_button, delete_button, export_button]:
            actions_layout.addWidget(button)
        root_layout.addLayout(actions_layout)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table = DataTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nr.", "Vorname", "Nachname", "Telefon", "E-Mail", "Erstellt am"])
        self.table.itemSelectionChanged.connect(self._handle_selection_changed)
        splitter.addWidget(self.table)

        self.detail_view = CustomerDetailView()
        splitter.addWidget(self.detail_view)
        splitter.setSizes([900, 420])
        root_layout.addWidget(splitter, 1)

    def refresh_data(self) -> None:
        with session_scope() as session:
            service = CustomerService(session)
            self.customers = service.list_customers(search=self.filter_bar.search_input.text())

        self.table.setRowCount(len(self.customers))
        for row, customer in enumerate(self.customers):
            self.table.setItem(row, 0, QTableWidgetItem(customer.customer_number))
            self.table.setItem(row, 1, QTableWidgetItem(customer.first_name))
            self.table.setItem(row, 2, QTableWidgetItem(customer.last_name))
            self.table.setItem(row, 3, QTableWidgetItem(customer.phone or "-"))
            self.table.setItem(row, 4, QTableWidgetItem(customer.email or "-"))
            self.table.setItem(row, 5, QTableWidgetItem(format_date(customer.created_at)))
        self.detail_view.set_customer(None)
        if self.customers:
            self.table.selectRow(0)

    def _current_customer(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.customers):
            return None
        return self.customers[row]

    def _handle_selection_changed(self) -> None:
        self.detail_view.set_customer(self._current_customer())

    def create_customer(self) -> None:
        with session_scope() as session:
            suggested_customer_number = CustomerService(session).get_next_customer_number()

        dialog = CustomerDialog(self, suggested_customer_number=suggested_customer_number)
        if dialog.exec():
            try:
                with session_scope() as session:
                    CustomerService(session).create_customer(dialog.get_data())
                self.refresh_data()
            except ValidationServiceError as exc:
                QMessageBox.warning(self, "Validierungsfehler", str(exc))

    def edit_customer(self) -> None:
        customer = self._current_customer()
        if not customer:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst einen Kunden auswählen.")
            return
        dialog = CustomerDialog(self, customer=customer)
        if dialog.exec():
            try:
                with session_scope() as session:
                    CustomerService(session).update_customer(customer.id, dialog.get_data())
                self.refresh_data()
            except (ValidationServiceError, EntityNotFoundError) as exc:
                QMessageBox.warning(self, "Fehler", str(exc))

    def delete_customer(self) -> None:
        customer = self._current_customer()
        if not customer:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst einen Kunden auswählen.")
            return
        if not ask_delete_confirmation(self, customer.full_name):
            return
        try:
            with session_scope() as session:
                CustomerService(session).delete_customer(customer.id)
            self.refresh_data()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"Kunde konnte nicht gelöscht werden:\n{exc}")

    def export_csv(self) -> None:
        rows = [
            [customer.customer_number, customer.first_name, customer.last_name, customer.phone or "", customer.email or ""]
            for customer in self.customers
        ]
        path = ExportService().export(
            filename=f"customers_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            headers=["Kundennummer", "Vorname", "Nachname", "Telefon", "E-Mail"],
            rows=rows,
        )
        QMessageBox.information(self, "Export erfolgreich", f"CSV-Datei wurde erstellt:\n{path}")
