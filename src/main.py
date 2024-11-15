import sys
from PyQt5.QtWidgets import QApplication
from product_rate_calculator import ProductRateCalculatorApp

def main():
    app = QApplication(sys.argv)
    window = ProductRateCalculatorApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
