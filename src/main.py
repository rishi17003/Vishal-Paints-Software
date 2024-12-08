import sys
from PyQt5.QtWidgets import QApplication
from HomeScreen import HomeScreen
from reportlab.pdfgen import canvas
from PyQt5.QtGui import QPixmap, QFont,QIcon
from product_rate_calculator import ProductRateCalculatorApp
from ProductHistoryScreen import ProductHistoryScreen

def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("vishal_icon.ico"))
    home_screen = HomeScreen()

    # Check if login was successful
    if home_screen.login_successful:  
        home_screen.show()  # Show the HomeScreen if login is successful
        app.exec()
    else:
        print("Login failed. Application exiting.")

    # window.show()
    # sys.exit(app.exec_())

if __name__ == "__main__":
    main()
