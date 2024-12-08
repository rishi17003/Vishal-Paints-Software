from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,
    QWidget, QFileDialog, QMessageBox, QHBoxLayout,QLineEdit, QLabel,QInputDialog,QScrollArea,QSizePolicy
)
# Correct import
from product_rate_calculator import ProductRateCalculatorApp

class ProductHistoryScreen(QWidget):
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        # product_rate_calculator = ProductRateCalculatorApp(db_connection)
        # # product_history_screen = ProductHistoryScreen(product_rate_calculator)
        # self.product_rate_calculator = product_rate_calculator
        self.product_rate_calculator = ProductRateCalculatorApp(db_connection)
        self.init_ui()

    from PyQt5.QtWidgets import QSizePolicy

    def init_ui(self):
        self.setWindowTitle("Product History")
        layout = QVBoxLayout()

        # Search Layout
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter product name to search...")
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_product_history)

        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        layout.addLayout(search_layout)

        # Table for product history
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels([
            "Product ID", "Product Name", "Description",
            "Yield", "Total Rate", "Date Created"
        ])

        # Set the table to expand and fill available space
        self.product_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Set minimum size for the table to make it bigger by default
        self.product_table.setMinimumHeight(600)  # Adjust height as needed
        self.product_table.setMinimumWidth(1000)  # Adjust width as needed

        layout.addWidget(self.product_table)

        # Fetch and display product history
        self.load_product_history()

        # Buttons Layout
        buttons_layout = QHBoxLayout()

        # Download Invoice button
        download_invoice_button = QPushButton("Download Costing Sheet")
        download_invoice_button.clicked.connect(self.download_invoice)
        buttons_layout.addWidget(download_invoice_button)

        import_button = QPushButton("Import Product")
        import_button.clicked.connect(self.import_product_data)
        buttons_layout.addWidget(import_button)

        multiply_button = QPushButton("Multiply Quantities")
        multiply_button.clicked.connect(self.multiply_quantities)
        buttons_layout.addWidget(multiply_button)

        # Back button
        back_button = QPushButton("Back")
        back_button.clicked.connect(self.close)
        buttons_layout.addWidget(back_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_product_history(self,search_query=None):
        """
        Loads product history from the database and displays it in the product history table.
        """
        try:
            # self.product_table.setRowCount(0)  # Remove all rows
            # self.product_table.clearContents()
            cursor = self.db_connection.cursor()
            if search_query:
                cursor.execute("""
                    SELECT id, product_name, description, yield, total_rate, created_date
                    FROM product_details
                    WHERE product_name LIKE ?
                    ORDER BY created_date DESC
                """, (f"%{search_query}%",))
            else:
                cursor.execute("""
                    SELECT id, product_name, description, yield, total_rate, created_date
                    FROM product_details
                    ORDER BY created_date DESC
                """)
            rows = cursor.fetchall()

            # self.product_table.setRowCount(0)

            # Populate product table
            self.product_table.setRowCount(len(rows))
            for row_idx, row_data in enumerate(rows):
                for col_idx, col_data in enumerate(row_data):
                    self.product_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load product history: {str(e)}")

    def search_product_history(self):
        """
        Filters the product history table based on the search input.
        """
        search_query = self.search_input.text().strip()
        self.load_product_history(search_query)

    def download_invoice(self):
        """
        Downloads an invoice for the selected product from the product history table.
        """
        try:
            selected_items = self.product_table.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "No Selection", "Please select a product to download the Costing Sheet.")
                return

            # Get selected product name (instead of product_id)
            row = selected_items[0].row()
            product_name = self.product_table.item(row, 1).text()  # product_name is in the second column

            # Fetch the invoice BLOB for the selected product using product_name
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT invoice_pdf
                FROM invoices
                WHERE product_name = ?
            """, (product_name,))
            invoice_data = cursor.fetchone()

            if not invoice_data or invoice_data[0] is None:
                QMessageBox.warning(self, "No Costing Sheet", "No Costing Sheet available for this product.")
                return

            # Get the invoice BLOB data
            invoice_blob = invoice_data[0]

            # Open a file dialog to choose save location
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save Costing Sheet", f"{product_name}.pdf", "PDF Files (*.pdf);;All Files (*)", options=options
            )

            if not file_path:
                return  # User canceled the save dialog

            # Save the BLOB data to the chosen file
            with open(file_path, 'wb') as file:
                file.write(invoice_blob)

            QMessageBox.information(self, "Success", f"Costing Sheet saved at: {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download Costing Sheet: {str(e)}")

    def import_product_data(self):
        """
        Import selected product details and open ProductRateCalculatorApp with pre-filled data.
        """
        selected_row = self.product_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a product to import.")
            return

        # Fetch product ID from the table
        product_id = int(self.product_table.item(selected_row, 0).text())
        print(f"Selected Product ID: {product_id}")
        
        # Query the product details from the product_details table
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM product_details WHERE id = ?', (product_id,))
        product_data = cursor.fetchone()

        if product_data is None:
            QMessageBox.warning(self, "Data Error", f"No data found for product ID: {product_id}")
            print("No data found for this product")  # Debugging output
            return

        print(f"Fetched Product Data: {product_data}")  # Debugging output

        # Query the raw materials linked to this product from the product_materials table
        cursor.execute('SELECT * FROM product_materials WHERE product_id = ?', (product_id,))
        raw_materials = cursor.fetchall()
        print(f"Fetched Raw Materials: {raw_materials}")  # Debugging output

        # Pass the data to the ProductRateCalculatorApp instance to populate fields
        self.product_rate_calculator.populate_data(product_data, raw_materials)
        self.product_rate_calculator.show()

    def multiply_quantities(self):
        """
        Multiply the quantities of raw materials for the selected product and open the ProductRateCalculatorApp with updated data.
        """
        selected_row = self.product_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a product to multiply quantities.")
            return

        # Get multiplication factor
        factor_input, ok = QInputDialog.getDouble(self, "Enter Multiplication Factor", "Factor:", 1.0, 0.1, 10000, 2)
        if not ok:
            return  # User cancelled

        # Fetch product ID from the table
        product_id = int(self.product_table.item(selected_row, 0).text())
        print(f"Selected Product ID: {product_id}")

        # Query the product details from the product_details table
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM product_details WHERE id = ?', (product_id,))
        product_data = cursor.fetchone()

        if product_data is None:
            QMessageBox.warning(self, "Data Error", f"No data found for product ID: {product_id}")
            return

        print(f"Fetched Product Data: {product_data}")

        # Query the raw materials linked to this product from the product_materials table
        cursor.execute('SELECT * FROM product_materials WHERE product_id = ?', (product_id,))
        raw_materials = cursor.fetchall()

        if not raw_materials:
            QMessageBox.warning(self, "No Raw Materials", f"No raw materials found for product ID: {product_id}")
            return

        # Multiply quantities of raw materials by the factor
        updated_raw_materials = []
        for material in raw_materials:
            material_name = material[3]
            current_quantity = material[4]
            rate=material[5]
            print(f"Material Data: {material}")
            print(f"Current quantity for material '{material_name}': {current_quantity}")
            print(f"Current quantity for material '{material_name}': {current_quantity}")

            try:
                current_quantity = float(current_quantity)
            except ValueError:
                QMessageBox.warning(self, "Data Error", f"Invalid quantity for material {material_name}")
                continue

            # Multiply the quantity by the factor
            new_quantity = current_quantity * factor_input
            updated_raw_materials.append((material_name,new_quantity,rate))

            # Update raw material quantities in the database
            cursor.execute('UPDATE product_materials SET quantity = ? WHERE id = ?', (new_quantity, material_name))

        # Commit changes to the database
        self.db_connection.commit()

        # Pass the updated data to the ProductRateCalculatorApp
        self.product_rate_calculator.update_material_quantities(updated_raw_materials)
        self.product_rate_calculator.show()

