import sys
import pyodbc
from PyQt5 import QtWidgets, QtGui, QtCore
from form2 import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection_string = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=DELL\\SQLEXPRESS;"
            "DATABASE=main;"
            "Trusted_Connection=yes;"
        )

        self.photo_data = None  # store raw image bytes

        # Connect buttons
        self.Uploadbtn.clicked.connect(self.upload_photo)
        self.pushButton.clicked.connect(self.save_data)  # "Submitt"
        self.searchbtn.clicked.connect(self.search_data)

        # Ensure table exists
        self.create_table()

    def create_table(self):
        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
                CREATE TABLE Users (
                    id INT IDENTITY PRIMARY KEY,
                    first_name NVARCHAR(100),
                    last_name NVARCHAR(100),
                    email NVARCHAR(255),
                    photo VARBINARY(MAX)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Could not create table:\n{e}")

    def upload_photo(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_path:
            with open(file_path, "rb") as file:
                self.photo_data = file.read()

            pixmap = QtGui.QPixmap(file_path).scaled(
                200, 100, QtCore.Qt.KeepAspectRatio
            )
            self.Photo.setPixmap(pixmap)

    def save_data(self):
        first_name = self.txtfname.text().strip()
        last_name = self.txtlname.text().strip()
        email = self.txtmail.text().strip()

        if not first_name or not last_name or not email:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (first_name, last_name, email, photo) VALUES (?, ?, ?, ?)",
                (first_name, last_name, email, self.photo_data)
            )
            conn.commit()
            conn.close()
            QMessageBox.information(self, "Success", "Data saved successfully.")
            self.clear_inputs()
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Could not save data:\n{e}")

    def search_data(self):
        search_text = self.txtsearch.text().strip()
        if not search_text:
            QMessageBox.warning(self, "Input Error", "Please enter a name or email to search.")
            return

        try:
            conn = pyodbc.connect(self.connection_string)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT first_name, last_name, email, photo
                FROM Users
                WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
            """, (f"%{search_text}%", f"%{search_text}%", f"%{search_text}%"))

            rows = cursor.fetchall()
            conn.close()

            self.tbresult.setRowCount(0)
            for row_data in rows:
                row_index = self.tbresult.rowCount()
                self.tbresult.insertRow(row_index)
                self.tbresult.setItem(row_index, 0, QtWidgets.QTableWidgetItem(row_data[0]))
                self.tbresult.setItem(row_index, 1, QtWidgets.QTableWidgetItem(row_data[1]))
                self.tbresult.setItem(row_index, 2, QtWidgets.QTableWidgetItem(row_data[2]))
                self.tbresult.setItem(row_index, 3, QtWidgets.QTableWidgetItem("Image stored"))

        except Exception as e:
            QMessageBox.critical(self, "Search Error", f"Could not search data:\n{e}")

    def clear_inputs(self):
        self.txtfname.clear()
        self.txtlname.clear()
        self.txtmail.clear()
        self.Photo.clear()
        self.photo_data = None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
