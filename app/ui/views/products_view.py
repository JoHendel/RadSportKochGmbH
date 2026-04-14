from __future__ import annotations

from datetime import datetime

from PySide6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QSplitter, QTableWidgetItem, QVBoxLayout, QWidget
from qfluentwidgets import ComboBox, PrimaryPushButton, PushButton

from app.core.enums import ProductCategory
from app.database.session import session_scope
from app.services.exceptions import EntityNotFoundError, ValidationServiceError
from app.services.export_service import ExportService
from app.services.product_service import ProductService
from app.ui.dialogs.confirm_dialog import ask_delete_confirmation
from app.ui.dialogs.product_dialog import ProductDialog
from app.ui.views.product_detail_view import ProductDetailView
from app.ui.widgets.filter_bar import FilterBar
from app.ui.widgets.table_widget import DataTableWidget
from app.utils.formatters import format_currency, format_date


class ProductsView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.products = []

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(24, 24, 24, 24)
        root_layout.setSpacing(16)

        title = QLabel("Artikelverwaltung")
        title.setProperty("role", "pageTitle")
        subtitle = QLabel("Behalte Sortiment, Preise und kritische Lagerbestände übersichtlich im Blick.")
        subtitle.setProperty("role", "pageSubtitle")
        root_layout.addWidget(title)
        root_layout.addWidget(subtitle)

        actions_layout = QHBoxLayout()
        self.filter_bar = FilterBar("Artikel suchen...")
        self.filter_bar.search_input.textChanged.connect(self.refresh_data)

        self.category_filter = ComboBox()
        self.category_filter.addItem("Alle Kategorien", None)
        for category in ProductCategory:
            self.category_filter.addItem(category.value, category)
        self.category_filter.currentIndexChanged.connect(self.refresh_data)
        self.filter_bar.add_labeled_widget("Kategorie", self.category_filter)
        actions_layout.addWidget(self.filter_bar, 1)

        add_button = PrimaryPushButton("Artikel anlegen")
        add_button.clicked.connect(self.create_product)
        edit_button = PushButton("Bearbeiten")
        edit_button.clicked.connect(self.edit_product)
        delete_button = PushButton("Löschen")
        delete_button.clicked.connect(self.delete_product)
        export_button = PushButton("CSV exportieren")
        export_button.clicked.connect(self.export_csv)
        for button in [add_button, edit_button, delete_button, export_button]:
            actions_layout.addWidget(button)
        root_layout.addLayout(actions_layout)

        splitter = QSplitter()
        self.table = DataTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Nr.", "Name", "Kategorie", "VK", "Bestand", "Mindestbestand", "Aktiv", "Erstellt am"]
        )
        self.table.itemSelectionChanged.connect(self._handle_selection_changed)
        splitter.addWidget(self.table)

        self.detail_view = ProductDetailView()
        splitter.addWidget(self.detail_view)
        splitter.setSizes([980, 420])
        root_layout.addWidget(splitter, 1)

    def refresh_data(self) -> None:
        with session_scope() as session:
            service = ProductService(session)
            self.products = service.list_products(
                search=self.filter_bar.search_input.text(),
                category=self.category_filter.currentData(),
            )

        self.table.setRowCount(len(self.products))
        for row, product in enumerate(self.products):
            self.table.setItem(row, 0, QTableWidgetItem(product.article_number))
            self.table.setItem(row, 1, QTableWidgetItem(product.name))
            self.table.setItem(row, 2, QTableWidgetItem(product.category.value))
            self.table.setItem(row, 3, QTableWidgetItem(format_currency(product.sale_price)))
            self.table.setItem(row, 4, QTableWidgetItem(str(product.stock_quantity)))
            self.table.setItem(row, 5, QTableWidgetItem(str(product.minimum_stock)))
            self.table.setItem(row, 6, QTableWidgetItem("Ja" if product.is_active else "Nein"))
            self.table.setItem(row, 7, QTableWidgetItem(format_date(product.created_at)))
        self.detail_view.set_product(None)
        if self.products:
            self.table.selectRow(0)

    def _current_product(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.products):
            return None
        return self.products[row]

    def _handle_selection_changed(self) -> None:
        self.detail_view.set_product(self._current_product())

    def create_product(self) -> None:
        dialog = ProductDialog(self)
        if dialog.exec():
            try:
                with session_scope() as session:
                    ProductService(session).create_product(dialog.get_data())
                self.refresh_data()
            except ValidationServiceError as exc:
                QMessageBox.warning(self, "Validierungsfehler", str(exc))

    def edit_product(self) -> None:
        product = self._current_product()
        if not product:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst einen Artikel auswählen.")
            return
        dialog = ProductDialog(self, product=product)
        if dialog.exec():
            try:
                with session_scope() as session:
                    ProductService(session).update_product(product.id, dialog.get_data())
                self.refresh_data()
            except (ValidationServiceError, EntityNotFoundError) as exc:
                QMessageBox.warning(self, "Fehler", str(exc))

    def delete_product(self) -> None:
        product = self._current_product()
        if not product:
            QMessageBox.information(self, "Hinweis", "Bitte zuerst einen Artikel auswählen.")
            return
        if not ask_delete_confirmation(self, product.name):
            return
        try:
            with session_scope() as session:
                ProductService(session).delete_product(product.id)
            self.refresh_data()
        except Exception as exc:
            QMessageBox.critical(self, "Fehler", f"Artikel konnte nicht gelöscht werden:\n{exc}")

    def export_csv(self) -> None:
        rows = [
            [
                product.article_number,
                product.name,
                product.category.value,
                f"{product.sale_price:.2f}",
                product.stock_quantity,
                product.minimum_stock,
                "Ja" if product.is_active else "Nein",
            ]
            for product in self.products
        ]
        path = ExportService().export(
            filename=f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            headers=["Artikelnummer", "Name", "Kategorie", "Verkaufspreis", "Bestand", "Mindestbestand", "Aktiv"],
            rows=rows,
        )
        QMessageBox.information(self, "Export erfolgreich", f"CSV-Datei wurde erstellt:\n{path}")
