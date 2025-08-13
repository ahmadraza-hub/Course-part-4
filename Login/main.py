# main.py
import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox
from login import Ui_MainWindow  # your login UI file
from cal import GorgeousCalculator  # your calculator file

USERNAME = "ahmad"
PASSWORD = "12345678"


class LoginApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.check_login)

    def check_login(self):
        username = self.txtfname.text().strip()
        password = self.txtlname.text().strip()

        if username == USERNAME and password == PASSWORD:
            self.open_calculator()
        else:
            QMessageBox.critical(self, "Login Failed", "Invalid username or password!")

    def open_calculator(self):
        self.calc_window = GorgeousCalculator()
        self.calc_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_window = LoginApp()
    login_window.show()
    sys.exit(app.exec_())
