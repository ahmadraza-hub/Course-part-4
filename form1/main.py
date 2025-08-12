import sys
import pyodbc
from PyQt5 import QtWidgets
from form1 import Ui_MainWindow  # Your converted UI file

# Change this to your SQL Server instance
SERVER = r"DELL\SQLEXPRESS"  # Example: DESKTOP-ABCD\SQLEXPRESS
DATABASE = "user"

class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pushButton.clicked.connect(self.save_data)

        self.conn = self.create_connection()
        if self.conn:
            self.create_table()
        else:
            QtWidgets.QMessageBox.critical(
                self, "Database Error", "Could not connect to the database."
            )

    def create_connection(self):
        try:
            # Step 1: Connect to master to ensure database exists
            temp_conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={SERVER};Trusted_Connection=yes;"
            )
            cursor = temp_conn.cursor()
            cursor.execute(f"IF DB_ID('{DATABASE}') IS NULL CREATE DATABASE [{DATABASE}]")
            temp_conn.commit()
            temp_conn.close()

            # Step 2: Connect to the target database
            conn = pyodbc.connect(
                f"DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;"
            )
            print("✅ Database connected")
            return conn
        except Exception as e:
            print("❌ Database connection failed:", e)
            return None

    def create_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
                CREATE TABLE Users (
                    ID INT PRIMARY KEY IDENTITY(1,1),
                    FirstName NVARCHAR(50),
                    LastName NVARCHAR(50),
                    Email NVARCHAR(100)
                )
            """)
            self.conn.commit()
            print("✅ Table ready")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

    def save_data(self):
        if not self.conn:
            QtWidgets.QMessageBox.critical(self, "Error", "No database connection.")
            return

        fname = self.txtfname.text().strip()
        lname = self.txtlname.text().strip()
        email = self.txtmail.text().strip()

        if not fname or not lname or not email:
            QtWidgets.QMessageBox.warning(self, "Input Error", "Please fill all fields.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO Users (FirstName, LastName, Email) VALUES (?, ?, ?)",
                (fname, lname, email)
            )
            self.conn.commit()
            QtWidgets.QMessageBox.information(self, "Success", "Data saved successfully.")
            self.txtfname.clear()
            self.txtlname.clear()
            self.txtmail.clear()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
