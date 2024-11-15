from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout, QGroupBox, QLineEdit, QPushButton, \
    QTableWidget, QTableWidgetItem, QLabel, QComboBox, QHBoxLayout, QMenuBar, QMenu, QAction, QMessageBox
import sqlite3

class ProductRateCalculatorApp(QMainWindow):  # Change to QMainWindow
    def __init__(self):
        super().__init__()
        self.initUI()
        self.db_connection = self.create_db_connection()
        self.create_raw_materials_table()
        self.create_product_details_table()

    def initUI(self):
        self.setWindowTitle("Product Rate Calculator")
        self.setGeometry(100, 100, 600, 600)

        # Create Menu Bar
        self.createMenuBar()

        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Product Details Form
        self.product_form = QFormLayout()
        self.product_form_group = QGroupBox("Product Details")
        layout.addWidget(self.product_form_group)

        self.product_name = QLineEdit()
        self.description = QLineEdit()
        self.yield_value = QLineEdit()
        self.viscosity = QLineEdit()
        self.weight_lit = QLineEdit()
        self.container_cost = QLineEdit()
        self.transport_cost = QLineEdit()
        self.sales_cost = QLineEdit()
        self.misc_cost = QLineEdit()
        self.total_rate = QLineEdit()

        self.product_form.addRow("Product Name:", self.product_name)
        self.product_form.addRow("Description:", self.description)
        self.product_form.addRow("Yield:", self.yield_value)
        self.product_form.addRow("Viscosity:", self.viscosity)
        self.product_form.addRow("Weight / Lit:", self.weight_lit)
        self.product_form.addRow("Container Cost:", self.container_cost)
        self.product_form.addRow("Transport Cost:", self.transport_cost)
        self.product_form.addRow("Sales Cost:", self.sales_cost)
        self.product_form.addRow("Miscellaneous Cost:", self.misc_cost)
        self.product_form.addRow("Total Rate:", self.total_rate)

        self.product_form_group.setLayout(self.product_form)

        # Add Materials Table
        self.material_table = QTableWidget(0, 4)
        self.material_table.setHorizontalHeaderLabels(
            ["Material Type", "Material Name", "Quantity", "Rate"]
        )
        layout.addWidget(QLabel("Materials:"))
        layout.addWidget(self.material_table)

        # Dropdown for material type and name
        self.material_type_dropdown = QComboBox()
        self.material_type_dropdown.addItems(["Pigment", "Additive", "Resin", "Thinner"])
        self.material_type_dropdown.currentIndexChanged.connect(self.update_material_name_dropdown)

        self.material_name_dropdown = QComboBox()  # Material Name dropdown (empty at first)
        self.quantity_input = QLineEdit()  # Quantity input field
        self.rate_input = QLineEdit()  # Rate input field (auto-populated)

        # Button to Add Material to Table
        self.add_material_button = QPushButton("Add Material")
        self.add_material_button.clicked.connect(self.add_material_to_table)

        # Layout for adding material inputs and button
        material_input_layout = QHBoxLayout()
        material_input_layout.addWidget(self.material_type_dropdown)
        material_input_layout.addWidget(self.material_name_dropdown)
        material_input_layout.addWidget(self.quantity_input)
        material_input_layout.addWidget(self.rate_input)
        material_input_layout.addWidget(self.add_material_button)

        layout.addLayout(material_input_layout)

        # Calculate Product Rate Button
        self.calculate_button = QPushButton("Calculate Product Rate")
        self.calculate_button.clicked.connect(self.calculate_product_rate)
        layout.addWidget(self.calculate_button)

        # Set Main Layout
        central_widget.setLayout(layout)

    def createMenuBar(self):
        menu_bar = self.menuBar()

        # Create Menus
        home_menu = menu_bar.addMenu('Home')
        product_menu = menu_bar.addMenu('Product')
        raw_material_menu = menu_bar.addMenu('Raw Material')
        inventory_menu = menu_bar.addMenu('Inventory')

        # Actions for Home Menu
        home_action = QAction('Home', self)
        home_action.triggered.connect(self.show_home)
        home_menu.addAction(home_action)

        # Actions for Product Menu
        product_rate_action = QAction('Product Rate Calculator', self)
        product_history_action = QAction('Product History', self)
        product_rate_action.triggered.connect(self.show_product_rate_calculator)
        product_history_action.triggered.connect(self.show_product_history)

        product_menu.addAction(product_rate_action)
        product_menu.addAction(product_history_action)

        # Actions for Raw Material Menu
        raw_material_management_action = QAction('Raw Material Management', self)
        raw_material_history_action = QAction('Raw Material History', self)
        raw_material_management_action.triggered.connect(self.show_raw_material_management)
        raw_material_history_action.triggered.connect(self.show_raw_material_history)

        raw_material_menu.addAction(raw_material_management_action)
        raw_material_menu.addAction(raw_material_history_action)

        # Actions for Inventory Menu
        inventory_details_action = QAction('Inventory Details', self)
        inventory_details_action.triggered.connect(self.show_inventory_details)

        inventory_menu.addAction(inventory_details_action)

    def show_home(self):
        QMessageBox.information(self, "Home", "You are at the Home screen.")

    def show_product_rate_calculator(self):
        QMessageBox.information(self, "Product Rate Calculator", "You are already on the Product Rate Calculator screen.")

    def show_product_history(self):
        QMessageBox.information(self, "Product History", "This feature will show the history of products.")

    def show_raw_material_management(self):
        QMessageBox.information(self, "Raw Material Management", "This feature will manage raw materials.")

    def show_raw_material_history(self):
        QMessageBox.information(self, "Raw Material History", "This feature will show the history of raw materials.")

    def show_inventory_details(self):
        QMessageBox.information(self, "Inventory Details", "This feature will show the inventory details.")

    def create_db_connection(self):
        """Create a connection to SQLite database"""
        conn = sqlite3.connect("product_rate.db")
        return conn

    def create_raw_materials_table(self):
        """Create the raw_materials table and insert initial data"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                mat_type TEXT NOT NULL
            )
        """)
        cursor.execute("""
            INSERT INTO raw_materials (name, price, mat_type) VALUES
            ('P1', 227.00, 'Pigment'),
            ('P11', 109.00, 'Pigment'),
            ('P6', 170.00, 'Pigment'),
            ('P3', 560.00, 'Pigment'),
            ('P4', 158.00, 'Pigment'),
            ('P5', 109.00, 'Pigment'),
            ('P60', 59.00, 'Pigment'),
            ('P7', 115.00, 'Pigment'),
            ('P100', 35.00, 'Pigment'),
            ('P50', 125.00, 'Pigment'),
            ('P70', 130.00, 'Pigment'),
            ('Redoxide Powder', 15.00, 'Pigment'),
            ('White Whiting', 25.00, 'Pigment'),
            ('Talc', 104.00, 'Pigment'),
            ('A1', 162.00, 'Additive'),
            ('A2', 150.00, 'Additive'),
            ('HCO', 150.00, 'Additive'),
            ('ACE', 600.00, 'Additive'),
            ('PINCOIL', 150.00, 'Additive'),
            ('BRIGHT', 600.00, 'Additive'),
            ('CATALYST MATT', 225.00, 'Additive'),
            ('ICLAY', 308.00, 'Additive'),
            ('ICLAY JELLY 10%', 250.00, 'Additive'),
            ('LEAK 10%', 108.00, 'Additive'),
            ('OMEGA', 55.00, 'Additive'),
            ('DH', 134.00, 'Additive'),
            ('M1 50%', 125.00, 'Resin'),
            ('M1 70%', 124.00, 'Resin'),
            ('M6', 206.00, 'Resin'),
            ('Mo 70%', 220.00, 'Resin'),
            ('MD', 129.00, 'Resin'),
            ('MD 60%', 125.00, 'Resin'),
            ('R 920', 160.00, 'Resin'),
            ('DBTL', 40.00, 'Resin'),
            ('927', 109.00, 'Resin'),
            ('X1', 118.00, 'Thinner'),
            ('X2', 120.00, 'Thinner'),
            ('X3', 118.00, 'Thinner'),
            ('X5', 105.00, 'Thinner'),
            ('C9', 38.00, 'Thinner'),
            ('C12', 25.00, 'Thinner');
        """)
        self.db_connection.commit()

    def create_product_details_table(self):
        """Create the product_details table"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_details (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_name TEXT NOT NULL,
                yield_value REAL NOT NULL,
                viscosity REAL NOT NULL,
                weight_lit REAL NOT NULL,
                container_cost REAL NOT NULL,
                transport_cost REAL NOT NULL,
                sales_cost REAL NOT NULL,
                misc_cost REAL NOT NULL,
                total_rate REAL NOT NULL
            )
        """)
        self.db_connection.commit()

    def update_material_name_dropdown(self):
        """Update the Material Name dropdown based on the selected material type"""
        selected_material_type = self.material_type_dropdown.currentText()
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT DISTINCT name FROM raw_materials WHERE mat_type = ?
        """, (selected_material_type,))
        material_names = cursor.fetchall()

        # Clear the existing entries in the material name dropdown
        self.material_name_dropdown.clear()

        # Add the new material names from the database
        self.material_name_dropdown.addItem("Select Material")
        for material_name in material_names:
            self.material_name_dropdown.addItem(material_name[0])

        # Automatically update rate when material name is selected
        self.material_name_dropdown.currentIndexChanged.connect(self.update_rate)

    def update_rate(self):
        """Fetch the rate from the database based on the selected material name"""
        selected_material_name = self.material_name_dropdown.currentText()
        if selected_material_name != "Select Material":
            cursor = self.db_connection.cursor()
            cursor.execute("""
                SELECT price FROM raw_materials WHERE name = ?
            """, (selected_material_name,))
            result = cursor.fetchone()
            if result:
                self.rate_input.setText(str(result[0]))

    def add_material_to_table(self):
        """Add material to the table and save to the database"""
        material_type = self.material_type_dropdown.currentText()
        material_name = self.material_name_dropdown.currentText()
        quantity = self.quantity_input.text()
        rate = self.rate_input.text()

        # Add to the table widget
        row_position = self.material_table.rowCount()
        self.material_table.insertRow(row_position)
        self.material_table.setItem(row_position, 0, QTableWidgetItem(material_type))
        self.material_table.setItem(row_position, 1, QTableWidgetItem(material_name))
        self.material_table.setItem(row_position, 2, QTableWidgetItem(quantity))
        self.material_table.setItem(row_position, 3, QTableWidgetItem(rate))

    def calculate_product_rate(self):
        """Calculate and display product rate"""
        # Collect all necessary information and calculate the rate
        total_cost = 0
        for row in range(self.material_table.rowCount()):
            quantity = float(self.material_table.item(row, 2).text())
            rate = float(self.material_table.item(row, 3).text())
            total_cost += quantity * rate

        self.total_rate.setText(str(total_cost))


if __name__ == "__main__":
    app = QApplication([])
    window = ProductRateCalculatorApp()
    window.show()
    app.exec_()
