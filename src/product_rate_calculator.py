from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QLabel, QComboBox, QFileDialog, QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox
from PyQt5.QtWidgets import (
      QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy,QGridLayout
     )
from PyQt5.QtWidgets import QCompleter, QTableWidgetItem
import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtGui import QStandardItem
from PyQt5.QtCore import Qt
import sqlite3
from PyQt5.QtWidgets import QDialog,QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel,QDoubleValidator
from PyQt5.QtWidgets import QAbstractItemView
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from datetime import datetime
from datetime import date
import os
# from ProductHistoryScreen import ProductHistoryScreen

class ProductRateCalculatorApp(QWidget):  # Change to QMainWindow
    def __init__(self, db_connection):
        super().__init__()
        self.db_connection = db_connection
        self.initUI()

    def create_raw_material_history_table(self):
        """Create the raw_material_history table if it does not exist"""
        cursor = self.db_connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS raw_material_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_material_id INTEGER NOT NULL,
            change_type TEXT NOT NULL,  -- e.g., 'added', 'updated', 'deleted'
            old_price REAL,
            new_price REAL,
            change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (raw_material_id) REFERENCES raw_materials (id)
        )
        ''')
        self.db_connection.commit()

    def initUI(self):
        self.setWindowTitle("Product Rate Calculator")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f4f9; /* Light pastel background for a clean look */
            }
            QGroupBox {
                font-size: 18px; /* Larger font size */
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif; /* Stylish font */
                color: #2c3e50; /* Deep gray for better visibility */
                border: 2px solid #bdc3c7; /* Subtle border */
                border-radius: 8px; /* Rounded edges */
                margin-top: 15px; /* Spacing above groups */
                padding: 10px; /* Internal padding for better readability */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 8px;
                font-size: 20px; /* Even larger font for titles */
                color: #34495e; /* Distinct title color */
            }
            QLabel {
                font-size: 16px; /* Slightly larger labels */
                font-family: 'Roboto', Arial, sans-serif; /* Modern font */
                color: #34495e; /* Distinct label color */
            }
            QLineEdit {
                border: 2px solid #95a5a6; /* Thicker border */
                border-radius: 5px; /* Rounded input boxes */
                padding: 10px;
                font-size: 16px; /* Larger text */
                font-family: 'Arial', sans-serif;
                background-color: #ffffff; /* White background */
                color: #2c3e50; /* Dark gray text */
            }
            QComboBox {
                border: 2px solid #95a5a6;
                border-radius: 5px;
                padding: 8px 10px;
                font-size: 16px;
                font-family: 'Arial', sans-serif;
                background-color: #ecf0f1; /* Light gray background */
                color: #2c3e50;
            }
            QPushButton {
            font-size: 14px; /* Reduced font size for buttons */
            padding: 8px 16px; /* Reduced padding */
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            font-family: 'Verdana', sans-serif;
            font-weight: bold;
        }
            QPushButton:hover {
                background-color: #2980b9; /* Darker blue on hover */
            }
            QPushButton:pressed {
                background-color: #1c598a; /* Even darker on click */
            }
            QTableWidget {
                border: 1px solid #bdc3c7;
                border-radius: 8px;
                background-color: #ffffff;
                font-size: 14px;
                font-family: 'Arial', sans-serif;
                color: #2c3e50;
            }
            QHeaderView::section {
                background-color: #34495e; /* Dark gray headers */
                color: white; /* White text for headers */
                font-weight: bold;
                font-size: 16px; /* Larger header font */
                border: none;
                padding: 8px;
            }
        """)

        
        # layout = QVBoxLayout(self)

        # # Product Details Form
        # self.product_form = QFormLayout()
        # self.product_form_group = QGroupBox("Product Details")
        # layout.addWidget(self.product_form_group)

        # product_form_layout = QVBoxLayout() 

        # self.operator_name = QLineEdit()
        # self.product_form.addRow("Operator Name:", self.operator_name)
        # self.product_name = QLineEdit()
        # self.description = QLineEdit()
        # self.yield_value = QLineEdit()
        # self.viscosity = QLineEdit()
        # self.weight_lit = QLineEdit()
        # self.container_cost = QLineEdit()
        # self.transport_cost = QLineEdit()
        # self.sales_cost = QLineEdit()
        # self.misc_cost = QLineEdit()
        # self.total_rate = QLineEdit()
        # self.total_rate.setReadOnly(True)

        # top_row_layout = QHBoxLayout()  # Horizontal layout for these three fields
        # self.operator_name.setFixedWidth(200)  # Increased width for operator name
        # self.product_name.setFixedWidth(200)  # Increased width for product name
        # self.description.setFixedWidth(200)  # Increased width for description

        # top_row_layout.addWidget(QLabel("Operator Name:"))
        # top_row_layout.addWidget(self.operator_name)
        # top_row_layout.addWidget(QLabel("Product Name:"))
        # top_row_layout.addWidget(self.product_name)
        # top_row_layout.addWidget(QLabel("Description:"))
        # top_row_layout.addWidget(self.description)

        # product_form_layout.addLayout(top_row_layout)

        # second_row_layout = QHBoxLayout()
        # self.yield_value.setFixedWidth(150)
        # self.viscosity.setFixedWidth(150)
        # self.weight_lit.setFixedWidth(150)

        # second_row_layout.addWidget(QLabel("Yield:"))
        # second_row_layout.addWidget(self.yield_value)
        # second_row_layout.addWidget(QLabel("Viscosity:"))
        # second_row_layout.addWidget(self.viscosity)
        # second_row_layout.addWidget(QLabel("Weight / Lit:"))
        # second_row_layout.addWidget(self.weight_lit)

        # product_form_layout.addLayout(second_row_layout)

        # # Third row - Container Cost, Transport Cost, Sales Cost, Miscellaneous Cost (slightly bigger fields)
        # third_row_layout = QHBoxLayout()
        # self.container_cost.setFixedWidth(150)
        # self.transport_cost.setFixedWidth(150)
        # self.sales_cost.setFixedWidth(150)
        # self.misc_cost.setFixedWidth(150)

        # third_row_layout.addWidget(QLabel("Container Cost:"))
        # third_row_layout.addWidget(self.container_cost)
        # third_row_layout.addWidget(QLabel("Transport Cost:"))
        # third_row_layout.addWidget(self.transport_cost)
        # third_row_layout.addWidget(QLabel("Sales Cost:"))
        # third_row_layout.addWidget(self.sales_cost)
        # third_row_layout.addWidget(QLabel("Miscellaneous Cost:"))
        # third_row_layout.addWidget(self.misc_cost)

        # product_form_layout.addLayout(third_row_layout)

        # # Fourth row - Total Rate (this one will be smaller)
        # total_row_layout = QHBoxLayout()
        # total_row_layout.addWidget(QLabel("Total Rate:"))
        # total_row_layout.addWidget(self.total_rate)
        # product_form_layout.addLayout(total_row_layout)

        # self.product_form_group.setLayout(product_form_layout)

        main_layout = QVBoxLayout(self)

    # Product Details Group
        self.product_form_group = QGroupBox("Product Details")
        product_form_layout = QGridLayout()  # Using a grid layout

        # Adding input fields with labels
        product_form_layout.addWidget(QLabel("Operator Name:"), 0, 0)
        self.operator_name = QLineEdit()
        product_form_layout.addWidget(self.operator_name, 0, 1)

        product_form_layout.addWidget(QLabel("Product Name:"), 0, 2)
        self.product_name = QLineEdit()
        product_form_layout.addWidget(self.product_name, 0, 3)

        product_form_layout.addWidget(QLabel("Description:"), 0, 4)
        self.description = QLineEdit()
        product_form_layout.addWidget(self.description, 0, 5)

        product_form_layout.addWidget(QLabel("Yield:"), 1, 0)
        self.yield_value = QLineEdit()
        product_form_layout.addWidget(self.yield_value, 1, 1)

        product_form_layout.addWidget(QLabel("Viscosity:"), 1, 2)
        self.viscosity = QLineEdit()
        product_form_layout.addWidget(self.viscosity, 1, 3)

        product_form_layout.addWidget(QLabel("Weight / Lit:"), 1, 4)
        self.weight_lit = QLineEdit()
        product_form_layout.addWidget(self.weight_lit, 1, 5)

        product_form_layout.addWidget(QLabel("Container Cost:"), 2, 0)
        self.container_cost = QLineEdit()
        product_form_layout.addWidget(self.container_cost, 2, 1)

        product_form_layout.addWidget(QLabel("Transport Cost:"), 2, 2)
        self.transport_cost = QLineEdit()
        product_form_layout.addWidget(self.transport_cost, 2, 3)

        product_form_layout.addWidget(QLabel("Sales Cost:"), 2, 4)
        self.sales_cost = QLineEdit()
        product_form_layout.addWidget(self.sales_cost, 2, 5)

        product_form_layout.addWidget(QLabel("Miscellaneous Cost:"), 3, 0)
        self.misc_cost = QLineEdit()
        product_form_layout.addWidget(self.misc_cost, 3, 1)

        product_form_layout.addWidget(QLabel("Total Rate:"), 3, 4)
        self.total_rate = QLineEdit()
        self.total_rate.setReadOnly(True)
        product_form_layout.addWidget(self.total_rate, 3, 5)

        self.product_form_group.setLayout(product_form_layout)
        main_layout.addWidget(self.product_form_group)

        


        # Dropdown for material type and name
        # self.material_type_dropdown = QComboBox()
        # self.material_type_label = QLabel("Select Material Type")
        # self.material_type_dropdown.addItems(["Pigment", "Additive", "Resin", "Thinner"])
        # self.material_type_dropdown.currentIndexChanged.connect(self.update_material_name_dropdown)

        # self.material_name_dropdown = QComboBox()
        # self.material_name_dropdown.setEditable(True)

        # # Use a model to allow filtering
        # self.material_name_model = QStandardItemModel(self.material_name_dropdown)
        # self.material_name_dropdown.setModel(self.material_name_model)

        # # Set a completer for filtering
        # completer = QCompleter(self.material_name_model, self)
        # completer.setFilterMode(Qt.MatchContains)  # Filter items containing the typed text
        # completer.setCompletionMode(QCompleter.PopupCompletion)
        # self.material_name_dropdown.setCompleter(completer)
        # self.material_name_dropdown.lineEdit().textChanged.connect(self.filter_material_names)

        # Populate the dropdown with all raw material names
        # self.populate_raw_material_names()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter Raw Material Name")
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_material)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        self.material_name_dropdown = QComboBox()
        self.populate_raw_material_names()  # Populate the dropdown with raw material names

        self.material_name_dropdown.currentIndexChanged.connect(self.update_rate)

        self.search_results_dropdown = QComboBox()
        self.search_results_dropdown.setVisible(False)  # Initially hidden
        self.search_results_dropdown.setEditable(False)
        self.search_results_dropdown.activated.connect(self.populate_main_dropdown)

        main_layout.addWidget(self.search_results_dropdown)



        main_layout.addWidget(QLabel("Select Material Name:"))
        main_layout.addWidget(self.material_name_dropdown)


        self.quantity_input = QLineEdit()  # Quantity input field
        self.rate_input = QLineEdit()  # Rate input field (auto-populated)

        # Button to Add Material to Table
        self.add_material_button = QPushButton("Add Material")
        self.add_material_button.clicked.connect(self.add_material_to_table)

        # Layout for adding material inputs and button
        material_input_layout = QHBoxLayout()
        # material_input_layout.addWidget(self.material_type_dropdown)
        material_input_layout.addWidget(self.material_name_dropdown)
        material_input_layout.addWidget(self.quantity_input)
        material_input_layout.addWidget(self.rate_input)
        material_input_layout.addWidget(self.add_material_button)

        main_layout.addLayout(material_input_layout)

        # Add Materials Table
        self.material_table = QTableWidget(0, 5)
        self.material_table.setHorizontalHeaderLabels(
            ["Material Name", "Quantity", "Rate", "", ""]
        )
        self.material_table.horizontalHeader().setStretchLastSection(True)  # Ensure columns stretch appropriately
        self.material_table.setColumnWidth(0, 250)  # Adjust material name column width
        self.material_table.setColumnWidth(1, 100)  # Adjust quantity column width
        self.material_table.setColumnWidth(2, 100)  # Adjust rate column width
        self.material_table.setColumnWidth(3, 120)  # Adjust save button column width
        self.material_table.setColumnWidth(4, 120)  # Adjust delete button column width
        self.material_table.resizeRowsToContents()

        main_layout.addWidget(QLabel("Materials:"))
        main_layout.addWidget(self.material_table)

        # # Calculate Product Rate Button
        # self.calculate_button = QPushButton("Calculate Product Rate")
        # self.calculate_button.setFixedSize(120, 40)
        # self.calculate_button.clicked.connect(self.calculate_product_rate)
        # layout.addWidget(self.calculate_button)

        # # Generate Invoice Button
        # self.invoice_button = QPushButton("Generate Costing Sheet") 
        # self.invoice_button.setFixedSize(120, 40)
        # self.invoice_button.clicked.connect(self.generate_invoice)
        # layout.addWidget(self.invoice_button)

        # # Clear Form Button
        # self.clear_button = QPushButton("Clear Form")
        # self.clear_button.setFixedSize(120, 40)
        # self.clear_button.clicked.connect(self.clear_form)
        # layout.addWidget(self.clear_button)

        button_layout = QHBoxLayout()

    # Calculate Product Rate Button
        self.calculate_button = QPushButton("Calculate Product Rate")
        self.calculate_button.setFixedSize(220, 40)  # Adjust size
        self.calculate_button.clicked.connect(self.calculate_product_rate)
        button_layout.addWidget(self.calculate_button)

        # Generate Invoice Button
        self.invoice_button = QPushButton("Generate Costing Sheet")
        self.invoice_button.setFixedSize(220, 40)  # Adjust size
        self.invoice_button.clicked.connect(self.generate_invoice)
        button_layout.addWidget(self.invoice_button)

        # Clear Form Button
        self.clear_button = QPushButton("Clear Form")
        self.clear_button.setFixedSize(140, 40)  # Adjust size
        self.clear_button.clicked.connect(self.clear_form)
        button_layout.addWidget(self.clear_button)

        main_layout.addLayout(button_layout)

    def populate_raw_material_names(self):
        """Populate the material name dropdown with all available raw material names."""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM raw_materials")
        material_names = cursor.fetchall()

        self.material_name_dropdown.clear()

        for material_name in material_names:
            self.material_name_dropdown.addItem(material_name[0])

    def search_material(self):
        """Search for raw materials starting with the entered letter and display them in the results dropdown."""
        search_text = self.search_input.text().strip().lower()
        if not search_text:
            return  # Don't search if the input is empty

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name, price FROM raw_materials WHERE name LIKE ?", (search_text + '%',))
        results = cursor.fetchall()

        # Clear previous search results and add new filtered items
        self.search_results_dropdown.clear()

        if results:
            for material_name, _ in results:
                self.search_results_dropdown.addItem(material_name)

            # Show the search results dropdown
            self.search_results_dropdown.setVisible(True)
        else:
            self.search_results_dropdown.setVisible(False)
            QMessageBox.information(self, "No Results", "No raw materials found matching the search criteria.")

    def populate_main_dropdown(self):
        """Populate the main raw material dropdown with the selected material and set its rate."""
        selected_material = self.search_results_dropdown.currentText()
        self.material_name_dropdown.setCurrentText(selected_material)

        # Fetch the rate for the selected material
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT price FROM raw_materials WHERE name = ?", (selected_material,))
        rate = cursor.fetchone()

        if rate:
            self.rate_input.setText(str(rate[0]))  # Assuming rate_input is your rate field
        else:
            self.rate_input.clear()

        # Hide the search results dropdown once a selection is made
        self.search_results_dropdown.setVisible(False)
    
    def clear_form(self):
        """
        Clears all input fields in the form.
        """
        self.product_name.clear()
        self.description.clear()
        self.yield_value.clear()
        self.viscosity.clear()
        self.weight_lit.clear()
        self.container_cost.clear()
        self.transport_cost.clear()
        self.sales_cost.clear()
        self.misc_cost.clear()
        self.total_rate.clear()
        self.material_table.setRowCount(0)

    def generate_invoice(self):
        """Generate and save an invoice as a PDF."""
        try:
            # Step 1: Get the product name from the QLineEdit
            product_name = self.product_name.text()  # Get the text value from the QLineEdit widget

            if not product_name:
                QMessageBox.warning(self, "No Product Name", "Product name cannot be empty.")
                return

            # Step 2: Define the folder where invoices will be stored
            folder_path = os.path.join(os.getcwd(), "Costing Sheets")  # Use the current working directory for the folder

            # Step 3: Create the folder if it doesn't exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Step 4: Set the file path using the product name and the folder path
            file_path = os.path.join(folder_path, f"{product_name}.pdf")

            # Optionally show a dialog to let the user confirm the file path
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Set Costing Sheet Download Path",
                file_path,  # Default path will now include product_name.pdf
                "PDF Files (*.pdf);;All Files (*)",
                options=options
            )

            if not file_path:
                QMessageBox.warning(self, "No Path Set", "No file path selected. Costing Sheet generation aborted.")
                return

            if not file_path.lower().endswith('.pdf'):
                file_path += ".pdf"

            # Step 5: Generate the PDF (implementation depends on your PDF generation logic)
            self.download_invoice(file_path)  # This method should implement the actual PDF generation

            QMessageBox.information(self, "Success", f"Costing Sheet saved at: {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while generating the invoice: {str(e)}")


    def download_invoice(self, file_path):
        """Generate and save the invoice as a PDF with proper alignment and structure."""
        operator_name = self.operator_name.text()
        product_name = self.product_name.text()
        product_description = self.description.text()
        total_rate = self.total_rate.text()

        if not product_name or not total_rate:
            QMessageBox.warning(self, "Error", "Please fill in product details and calculate the rate first!")
            return

        pdf_canvas = canvas.Canvas(file_path, pagesize=A4)
        pdf_canvas.setTitle(f"Costing Sheet - {product_name}")
        width, height = A4

        # Header: Product Name and Description
        pdf_canvas.setFont("Helvetica-Bold", 16)
        pdf_canvas.drawString(50, height - 50, "Vishal Paints, Inc")
        pdf_canvas.setFont("Helvetica-Bold", 14)
        pdf_canvas.drawString(50, height - 80, f"Product: {product_name}")
        pdf_canvas.setFont("Helvetica", 12)
        pdf_canvas.drawString(50, height - 100, f"Description: {product_description}")
        pdf_canvas.drawString(50, height - 120, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
        pdf_canvas.drawString(50, height - 140, f"Operator: {operator_name}")


        # Calculate details (previous calculation logic remains the same)
        yield_amount = float(self.yield_value.text() or 0)
        viscosity = self.viscosity.text()
        weight_lit = float(self.weight_lit.text() or 0)
        container_cost = float(self.container_cost.text() or 0)
        transport_cost = float(self.transport_cost.text() or 0)
        sales_cost = float(self.sales_cost.text() or 0)
        misc_cost = float(self.misc_cost.text() or 0)

        additive_cost, resin_cost, pigment_cost, thinner_cost,tinter_cost = 0, 0, 0, 0, 0
        invoice_items = []
        total_quantity = 0
        total = 0

        for row in range(self.material_table.rowCount()):
            material_name = self.material_table.item(row, 0).text()
            quantity = float(self.material_table.item(row, 1).text() or 0)
            rate_per_unit = float(self.material_table.item(row, 2).text() or 0)
            total_cost = quantity * rate_per_unit
            total+=total_cost
            total_quantity+=quantity
            cursor = self.db_connection.cursor()
            cursor.execute("SELECT mat_type FROM raw_materials WHERE name = ?", (material_name,))
            material_type_result = cursor.fetchone()


            
            # Debug material details
            print(f"Material: {material_name}, Quantity: {quantity}, Rate: {rate_per_unit}, Total Cost: {total_cost}")
            print(f"Material Type: {material_type_result}")
            
            if material_type_result:
                # Unpack the material type
                material_type = material_type_result[0]  # Extract the string from the tuple
                print(total_cost)
                # Accumulate costs based on the material type
                if material_type == 'Additive':
                    additive_cost += total_cost
                elif material_type == 'Resin':
                    resin_cost += total_cost
                elif material_type == 'Pigment':
                    pigment_cost += total_cost
                elif material_type == 'Thinner':
                    thinner_cost += total_cost
                elif material_type == 'Tinter':
                    tinter_cost += total_cost
                

                invoice_items.append((material_name, quantity, rate_per_unit, total_cost))
                # Debug updated costs
                print(f"Updated Costs -> Additive: {additive_cost}, Resin: {resin_cost}, Pigment: {pigment_cost}, Thinner: {thinner_cost}, Tinter: {tinter_cost}")


        rate_per_kg = float(total) / total_quantity if total_quantity > 0 else 0
        rate_per_lit = float(total) / yield_amount if yield_amount > 0 else 0
        cost_per_lit = rate_per_lit + container_cost + transport_cost + sales_cost + misc_cost




        # Previous calculation logic for invoice items and costs...

        # Positioning and Spacing Improvements
        top_margin = 50  # Left margin
        right_margin = width - 300  # Adjusted right margin
        details_spacing = 20  # Spacing between details

        # Calculate available page height
        usable_height = height - 200  # Reserve space for header

        # Detailed Section Positioning
        y_position = height - 160

        # Left Details Column
        left_details = [
            f"Yield: {yield_amount}",
            f"Viscosity: {viscosity}",
            f"Weight/Lit: {weight_lit}",
        ]
        for detail in left_details:
            pdf_canvas.drawString(top_margin, y_position, detail)
            y_position -= details_spacing

        # Right Details Column
        y_position = height - 160
        right_details = [
            f"Container Cost: Rs {container_cost}",
            f"Transport Cost: Rs {transport_cost}",
            f"Sales Cost: Rs {sales_cost}",
            f"Misc. Cost: Rs {misc_cost}",
        ]
        for detail in right_details:
            pdf_canvas.drawString(right_margin, y_position, detail)
            y_position -= details_spacing


        # Table Data Preparation
        table_data = [["Material Name", "Quantity", "Rate/Unit (Rs)", "Total Cost (Rs)"]]
        for item in invoice_items:
            table_data.append([item[0], f"{item[1]:.3f}", f"{item[2]:.3f}", f"{item[3]:.3f}"])
        table_data.append(["", f"Total: {total_quantity:.3f}", "", f"Total: Rs {total:.3f}"])

        # Dynamic Table Sizing
        table_width = width - (2 * top_margin)  # Full width minus margins
        col_widths = [
            table_width * 0.4,  # Material Name: 40%
            table_width * 0.2,  # Quantity: 20%
            table_width * 0.2,  # Rate/Unit: 20%
            table_width * 0.2,  # Total Cost: 20%
        ]


        # Create Table with Dynamic Widths
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        # Calculate table height and adjust positioning
        # table_height = 0
        table.wrapOn(pdf_canvas, table_width, height)
        table_height = table._height

        # Position table with sufficient spacing
        table_y_position = height - 250 - table_height
        table.drawOn(pdf_canvas, top_margin, table_y_position)

      # Summary Section Positioning
        # y_position = table_y_position - 50  # Space below table
        # left_summary = [
        #     f"Additive Cost/Lit: Rs {additive_cost / yield_amount:.3f}" if yield_amount else "Additive Cost/Lit: N/A",
        #     f"Resin Cost/Lit: Rs {resin_cost / yield_amount:.3f}" if yield_amount else "Resin Cost/Lit: N/A",
        #     f"Pigment Cost/Lit: Rs {pigment_cost / yield_amount:.3f}" if yield_amount else "Pigment Cost/Lit: N/A",
        #     f"Thinner Cost/Lit: Rs {thinner_cost / yield_amount:.3f}" if yield_amount else "Thinner Cost/Lit: N/A",
        #     f"Tinter Cost/Lit: Rs {tinter_cost / yield_amount:.3f}" if yield_amount else "Tinter Cost/Lit: N/A",
        # ]
        # for cost_type, value in zip(['Additive', 'Resin', 'Pigment', 'Thinner', 'Tinter'], 
        #                     [additive_cost, resin_cost, pigment_cost, thinner_cost, tinter_cost]):
        #     print(f"{cost_type} Cost: {value}, Yield Amount: {yield_amount}")
        # right_summary = [
        #     f"Rate/Kg: Rs {rate_per_kg:.3f}" if rate_per_kg else "Rate/Kg: N/A",
        #     f"Rate/Lit: Rs {rate_per_lit:.3f}" if rate_per_lit else "Rate/Lit: N/A",
        #     f"Cost/Lit: Rs {cost_per_lit:.3f}" if cost_per_lit else "Cost/Lit: N/A",
        # ]

        # # Ensure there is enough space
        # if y_position < 50:
        #     pdf_canvas.showPage()
        #     y_position = height - 100

        # for left, right in zip(left_summary, right_summary):
        #     pdf_canvas.drawString(top_margin, y_position, left)
        #     pdf_canvas.drawString(width - 200, y_position, right)
        #     y_position -= 20


        # Summary Section Positioning
        y_position = table_y_position - 50  # Space below table
        summary_details = [
            f"Additive Cost/Lit: Rs {additive_cost / yield_amount:.3f}" if yield_amount else "Additive Cost/Lit: N/A",
            f"Resin Cost/Lit: Rs {resin_cost / yield_amount:.3f}" if yield_amount else "Resin Cost/Lit: N/A",
            f"Pigment Cost/Lit: Rs {pigment_cost / yield_amount:.3f}" if yield_amount else "Pigment Cost/Lit: N/A",
            f"Thinner Cost/Lit: Rs {thinner_cost / yield_amount:.3f}" if yield_amount else "Thinner Cost/Lit: N/A",
            f"Tinter Cost/Lit: Rs {tinter_cost / yield_amount:.3f}" if yield_amount else "Tinter Cost/Lit: N/A",
            f"Rate/Kg: Rs {rate_per_kg:.3f}" if rate_per_kg else "Rate/Kg: N/A",
            f"Rate/Lit: Rs {rate_per_lit:.3f}" if rate_per_lit else "Rate/Lit: N/A",
            f"Cost/Lit: Rs {cost_per_lit:.3f}" if cost_per_lit else "Cost/Lit: N/A",
        ]

        # Ensure there is enough space for details
        if y_position < len(summary_details) * 20:  # Check if all details fit, otherwise start a new page
            pdf_canvas.showPage()
            y_position = height - 100

        for detail in summary_details:
            pdf_canvas.drawString(top_margin, y_position, detail)
            y_position -= 20


            # Save the PDF
        pdf_canvas.save()


    def save_product_and_materials_to_database(self):
        """
        Save product and associated raw material details to the database.
        """
        try:
            cursor = self.db_connection.cursor()

            # Save product details
            cursor.execute('''
                INSERT INTO products_invoice (product_name, description, operator_name, yield, viscosity, weight_per_lit,
                                    container_cost, transport_cost, sales_cost, misc_cost, total_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                self.product_name.text(),
                self.description.text(),
                self.operator_name.text(),
                float(self.yield_value.text() or 0),
                self.viscosity.text(),
                float(self.weight_lit.text() or 0),
                float(self.container_cost.text() or 0),
                float(self.transport_cost.text() or 0),
                float(self.sales_cost.text() or 0),
                float(self.misc_cost.text() or 0),
                float(self.total_rate.text() or 0)
            ))
            product_id = cursor.lastrowid

            # Save raw material details
            for row in range(self.material_table.rowCount()):
                material_type = self.material_table.item(row, 0).text()
                material_name = self.material_table.item(row, 1).text()
                quantity = float(self.material_table.item(row, 2).text() or 0)
                rate = float(self.material_table.item(row, 3).text() or 0)

                cursor.execute('''
                    INSERT INTO raw_materials_invoice (product_id, material_type, material_name, quantity, rate)
                    VALUES (?, ?, ?, ?, ?)
                ''', (product_id, material_type, material_name, quantity, rate))

            self.db_connection.commit()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Failed to save product details: {str(e)}")


    # def update_material_type_dropdown(self):
    #     """Populate the Material Type dropdown with available material types."""
    #     cursor = self.db_connection.cursor()
    #     cursor.execute("SELECT DISTINCT mat_type FROM raw_materials")
    #     material_types = cursor.fetchall()

    #     self.material_type_dropdown.clear()

    #     # Add placeholder item
    #     self.material_type_dropdown.addItem("Select Material Type")
    #     for material_type in material_types:
    #         self.material_type_dropdown.addItem(material_type[0])

    #     # Connect to material name update function
    #     self.material_type_dropdown.currentIndexChanged.connect(self.update_material_name_dropdown)

    # def update_material_name_dropdown(self):
    #     """Update the Material Name dropdown based on the selected material type."""
    #     selected_material_type = self.material_type_dropdown.currentText()

    #     # Skip if the placeholder is selected
    #     if selected_material_type == "Select Material Type":
    #         self.material_name_dropdown.clear()
    #         self.material_name_dropdown.addItem("Select Material")
    #         return

    #     cursor = self.db_connection.cursor()
    #     cursor.execute("""
    #         SELECT DISTINCT name FROM raw_materials WHERE mat_type = ?
    #     """, (selected_material_type,))
    #     material_names = cursor.fetchall()

    #     self.material_name_dropdown.clear()

    #     # Add placeholder item
    #     # self.material_name_dropdown.addItem("Select Material")
    #     for material_name in material_names:
    #         self.material_name_dropdown.addItem(material_name[0])

    #     # Connect to rate update function
    #     self.material_name_dropdown.currentIndexChanged.connect(self.update_rate)

    def update_rate(self):
        """Fetch the rate from the database based on the selected material name"""
        selected_material_name = self.material_name_dropdown.currentText()
        
        # Check if a valid material name is selected
        if selected_material_name:
            cursor = self.db_connection.cursor()
            cursor.execute("""SELECT price FROM raw_materials WHERE name = ?""", (selected_material_name,))
            result = cursor.fetchone()
            
            if result:  # If a rate is found for the selected material
                self.rate_input.setText(str(result[0]))  # Set the rate in the rate input field
            else:
                self.rate_input.clear()  # Clear the rate input if no rate is found


    def add_material_to_table(self):
        """Add material to table with quantity and rate."""
        material_name = self.material_name_dropdown.currentText()
        quantity = self.quantity_input.text()
        rate = self.rate_input.text()
        
        row_position = self.material_table.rowCount()
        self.material_table.insertRow(row_position)

        self.material_table.setItem(row_position, 0, QTableWidgetItem(material_name))
        self.material_table.setItem(row_position, 1, QTableWidgetItem(quantity))
        self.material_table.setItem(row_position, 2, QTableWidgetItem(rate))

        save_button = QPushButton("Save")
        save_button.setFixedSize(100, 50)
        save_button.clicked.connect(lambda: self.save_material(row_position))
        self.material_table.setCellWidget(row_position, 3, save_button)

        # Add Delete button
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 50)
        delete_button.clicked.connect(lambda: self.delete_material(row_position))
        self.material_table.setCellWidget(row_position, 4, delete_button)

        self.material_table.setColumnWidth(3, 120)  # Save column width
        self.material_table.setColumnWidth(4, 120)
        self.material_table.resizeRowsToContents()
        self.quantity_input.clear()

    def save_material(self, row):
        """Save updated quantity and rate for a material."""
        try:
            material_name = self.material_table.item(row, 0).text()
            quantity = self.material_table.item(row, 1).text()
            rate = self.material_table.item(row, 2).text()

            # Update the database
            cursor = self.db_connection.cursor()
            cursor.execute("""
                UPDATE product_materials
                SET quantity = ?, rate = ?
                WHERE material_name = ?
            """, (quantity, rate, material_name))
            self.db_connection.commit()

            QMessageBox.information(self, "Success", f"Updated {material_name}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save material: {str(e)}")

    def delete_material(self, row):
        """Delete a material from the table and database."""
        try:
            material_name = self.material_table.item(row, 0).text()

            # Delete from database
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM product_materials WHERE material_name = ?", (material_name,))
            self.db_connection.commit()

            # Remove row from the table
            self.material_table.removeRow(row)

            QMessageBox.information(self, "Success", f"Deleted {material_name}.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to delete material: {str(e)}")


    def calculate_product_rate(self):
        """Calculate, display, and commit the total product rate to the database."""
        try:
            # Calculate total material cost from the table
            total_material_cost = 0
            for row in range(self.material_table.rowCount()):
                quantity = float(self.material_table.item(row, 1).text())
                rate = float(self.material_table.item(row, 2).text())
                total_material_cost += quantity * rate

            # Collect additional product costs
            container_cost = float(self.container_cost.text() or 0)
            transport_cost = float(self.transport_cost.text() or 0)
            sales_cost = float(self.sales_cost.text() or 0)
            misc_cost = float(self.misc_cost.text() or 0)

            # Calculate total rate
            total_cost = total_material_cost + container_cost + transport_cost + sales_cost + misc_cost
            self.total_rate_value = total_cost  # Store the total rate for later use

            # Display the total rate in a field
            self.total_rate.setText(f"{total_cost:.3f}")  # Update UI field

            # Gather product details
            operator_name=self.operator_name.text()
            product_name = self.product_name.text()
            description = self.description.text()
            yield_value = float(self.yield_value.text() or 0)
            viscosity = float(self.viscosity.text() or 0)
            weight_lit = float(self.weight_lit.text() or 0)
            date_created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Commit product details and calculated rate to the database
            cursor = self.db_connection.cursor()
            cursor.execute("""
                INSERT INTO product_details (
                    operator_name,product_name,description,yield, viscosity, weight_per_lit, container_cost,
                    transport_cost, sales_cost, misc_cost, total_rate,created_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                operator_name,product_name, description, yield_value, viscosity, weight_lit, container_cost,
                transport_cost, sales_cost, misc_cost, total_cost,date_created
            ))
            product_id = cursor.lastrowid
            self.db_connection.commit()

            for row in range(self.material_table.rowCount()):
                # material_type = self.material_table.item(row, 0).text()
                material_name = self.material_table.item(row, 0).text()
                quantity = float(self.material_table.item(row, 1).text() or 0)
                rate = float(self.material_table.item(row, 2).text() or 0)

                cursor.execute(''' select mat_type from raw_materials where name= ? ''',(material_name,))
                material_type_result = cursor.fetchone()

                if material_type_result:
                    material_type = material_type_result[0]  # Fetch the material type

            # Insert each material detail into the product_materials table
                cursor.execute("""
                    INSERT INTO product_materials (product_id, material_type, material_name, quantity, rate)
                    VALUES (?, ?, ?, ?, ?)
                """, (product_id, material_type, material_name, quantity, rate))
        
            self.db_connection.commit()

            # Show confirmation message
            QMessageBox.information(self, "Success", "Product rate calculated and saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while calculating the product rate:\n{str(e)}")

    def populate_data(self, product_data, raw_materials):
        """
        Populate the form fields with the imported product data.
        """
        self.clear_form()
        self.material_table.setRowCount(0)

        # Assuming product_data is a tuple and the fields are in the following order:
        # id, product_name, description, operator_name, yield_value, viscosity, weight_per_lit,
        # container_cost, transport_cost, sales_cost, misc_cost, total_rate, date_created
        self.product_name.setText(product_data[2])  # product_name
        self.description.setText(product_data[3])  # description
        self.operator_name.setText(product_data[1])  # operator_name
        self.yield_value.setText(str(product_data[4]))  # yield_value
        self.viscosity.setText(product_data[5])  # viscosity
        self.weight_lit.setText(str(product_data[6]))  # weight_per_lit
        self.container_cost.setText(str(product_data[7]))  # container_cost
        self.transport_cost.setText(str(product_data[8]))  # transport_cost
        self.sales_cost.setText(str(product_data[9]))  # sales_cost
        self.misc_cost.setText(str(product_data[10]))  # misc_cost
        self.total_rate.setText(str(product_data[11]))  # total_rate

        # Populate the raw materials table
        
        # for material in raw_materials:
        #     row = self.material_table.rowCount()
        #     self.material_table.insertRow(row)
        #     self.material_table.setItem(row, 0, QTableWidgetItem(material[3]))  # material_name
        #     self.material_table.setItem(row, 1, QTableWidgetItem(str(material[4])))  # quantity
        #     self.material_table.setItem(row, 2, QTableWidgetItem(str(material[5])))  # rate

        # save_button = QPushButton("Save")
        # save_button.setFixedSize(100, 50)
        # save_button.clicked.connect(lambda _, row: self.save_material(row))
        # self.material_table.setCellWidget(row, 3, save_button)

        # delete_button = QPushButton("Delete")
        # delete_button.setFixedSize(100, 50)
        # delete_button.clicked.connect(lambda _, row: self.delete_material(row))
        # self.material_table.setCellWidget(row, 4, delete_button)

        for i, material in enumerate(raw_materials):
        # Add a new row to the table
            self.material_table.insertRow(i)

            # Populate columns for the row
            self.material_table.setItem(i, 0, QTableWidgetItem(material[3]))  # Material name
            self.material_table.setItem(i, 1, QTableWidgetItem(str(material[4])))  # Quantity
            self.material_table.setItem(i, 2, QTableWidgetItem(str(material[5])))  # Rate

        # Add Save button
            save_button = QPushButton("Save")
            save_button.setFixedSize(100, 50)
            save_button.clicked.connect(self.create_save_handler(i))  # Use helper to bind the row
            self.material_table.setCellWidget(i, 3, save_button)

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.setFixedSize(100, 50)
            delete_button.clicked.connect(self.create_delete_handler(i))  # Use helper to bind the row
            self.material_table.setCellWidget(i, 4, delete_button)

    def create_save_handler(self, row):
        """Helper to create a save handler with row binding."""
        return lambda: self.save_material(row)

    def create_delete_handler(self, row):
        """Helper to create a delete handler with row binding."""
        return lambda: self.delete_material(row)

    def update_material_quantities(self, updated_raw_materials):
        """Update the material quantities in the table after multiplication."""
        # Clear existing rows first
        self.material_table.setRowCount(0)

        for i, material in enumerate(updated_raw_materials):
            self.material_table.insertRow(i)

            # Populate columns for the row
            self.material_table.setItem(i, 0, QTableWidgetItem(material[0]))  # Material name
            self.material_table.setItem(i, 1, QTableWidgetItem(str(material[1])))  # Quantity
            self.material_table.setItem(i, 2, QTableWidgetItem(str(material[2])))  # Rate

            # Add Save and Delete buttons
            save_button = QPushButton("Save")
            save_button.setFixedSize(100, 50)
            save_button.clicked.connect(self.create_save_handler(i))  # Use helper to bind the row
            self.material_table.setCellWidget(i, 3, save_button)

            # Add Delete button
            delete_button = QPushButton("Delete")
            delete_button.setFixedSize(100, 50)
            delete_button.clicked.connect(self.create_delete_handler(i))  # Use helper to bind the row
            self.material_table.setCellWidget(i, 4, delete_button)
