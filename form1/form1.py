import sys
import pyodbc
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(763, 454)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.Background = QtWidgets.QLabel(self.centralwidget)
        self.Background.setGeometry(QtCore.QRect(-270, -130, 1601, 861))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Background.setFont(font)
        self.Background.setStyleSheet("background-color: #2C2F33 ;")
        self.Background.setText("")
        self.Background.setAlignment(QtCore.Qt.AlignCenter)
        self.Background.setObjectName("Background")

        self.Heading = QtWidgets.QLabel(self.centralwidget)
        self.Heading.setGeometry(QtCore.QRect(290, 0, 191, 81))
        self.Heading.setAlignment(QtCore.Qt.AlignCenter)
        self.Heading.setObjectName("Heading")

        self.Fname = QtWidgets.QLabel(self.centralwidget)
        self.Fname.setGeometry(QtCore.QRect(0, 90, 161, 81))
        self.Fname.setAlignment(QtCore.Qt.AlignCenter)
        self.Fname.setObjectName("Fname")

        self.Lname = QtWidgets.QLabel(self.centralwidget)
        self.Lname.setGeometry(QtCore.QRect(0, 170, 161, 81))
        self.Lname.setAlignment(QtCore.Qt.AlignCenter)
        self.Lname.setObjectName("Lname")

        self.Email = QtWidgets.QLabel(self.centralwidget)
        self.Email.setGeometry(QtCore.QRect(-40, 250, 191, 91))
        self.Email.setAlignment(QtCore.Qt.AlignCenter)
        self.Email.setObjectName("Email")

        self.txtfname = QtWidgets.QLineEdit(self.centralwidget)
        self.txtfname.setGeometry(QtCore.QRect(230, 110, 371, 41))
        self.txtfname.setObjectName("txtfname")

        self.txtmail = QtWidgets.QLineEdit(self.centralwidget)
        self.txtmail.setGeometry(QtCore.QRect(230, 270, 371, 41))
        self.txtmail.setObjectName("txtmail")

        self.txtlname = QtWidgets.QLineEdit(self.centralwidget)
        self.txtlname.setGeometry(QtCore.QRect(230, 190, 371, 41))
        self.txtlname.setObjectName("txtlname")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 350, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(85, 85, 255); color: white;")
        self.pushButton.setObjectName("pushButton")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Heading.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; font-style:italic; color:#ffffff;\">FORM 1</span></p></body></html>"))
        self.Fname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">First Name</span></p></body></html>"))
        self.Lname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">Last Name</span></p></body></html>"))
        self.Email.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">Email</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Submit"))

# =========================================
# Main Application Class
# =========================================
class MainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Connect to SQL Server
        try:
            self.conn = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server};'
                'SERVER=DELL\\SQLEXPRESS;'
                'DATABASE=user;'
                'Trusted_Connection=yes;'
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Could not connect to database:\n{e}")
            sys.exit(1)

        # Connect button to function
        self.pushButton.clicked.connect(self.insert_data)

    def insert_data(self):
        fname = self.txtfname.text().strip()
        lname = self.txtlname.text().strip()
        email = self.txtmail.text().strip()

        if fname and lname and email:
            try:
                self.cursor.execute(
                    "INSERT INTO Users (Name, Email) VALUES (?, ?)",
                    (fname + " " + lname, email)
                )
                self.conn.commit()
                QtWidgets.QMessageBox.information(self, "Success", "Data inserted successfully!")

                # Clear input fields
                self.txtfname.clear()
                self.txtlname.clear()
                self.txtmail.clear()

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to insert data:\n{e}")
        else:
            QtWidgets.QMessageBox.warning(self, "Missing Data", "Please enter all fields.")

# =========================================
# Run Application
# =========================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())










































































# from PyQt5 import QtCore, QtGui, QtWidgets


# class Ui_MainWindow(object):
#     def setupUi(self, MainWindow):
#         MainWindow.setObjectName("MainWindow")
#         MainWindow.resize(763, 454)
#         self.centralwidget = QtWidgets.QWidget(MainWindow)
#         self.centralwidget.setObjectName("centralwidget")
#         self.Background = QtWidgets.QLabel(self.centralwidget)
#         self.Background.setGeometry(QtCore.QRect(-270, -130, 1601, 861))
#         font = QtGui.QFont()
#         font.setPointSize(18)
#         font.setBold(True)
#         font.setItalic(True)
#         font.setWeight(75)
#         self.Background.setFont(font)
#         self.Background.setStyleSheet("background-color: #2C2F33 ;")
#         self.Background.setText("")
#         self.Background.setAlignment(QtCore.Qt.AlignCenter)
#         self.Background.setObjectName("Background")
#         self.Heading = QtWidgets.QLabel(self.centralwidget)
#         self.Heading.setGeometry(QtCore.QRect(290, 0, 191, 81))
#         self.Heading.setAlignment(QtCore.Qt.AlignCenter)
#         self.Heading.setObjectName("Heading")
#         self.Fname = QtWidgets.QLabel(self.centralwidget)
#         self.Fname.setGeometry(QtCore.QRect(0, 90, 161, 81))
#         self.Fname.setAlignment(QtCore.Qt.AlignCenter)
#         self.Fname.setObjectName("Fname")
#         self.Lname = QtWidgets.QLabel(self.centralwidget)
#         self.Lname.setGeometry(QtCore.QRect(0, 170, 161, 81))
#         self.Lname.setAlignment(QtCore.Qt.AlignCenter)
#         self.Lname.setObjectName("Lname")
#         self.Email = QtWidgets.QLabel(self.centralwidget)
#         self.Email.setGeometry(QtCore.QRect(-40, 250, 191, 91))
#         self.Email.setAlignment(QtCore.Qt.AlignCenter)
#         self.Email.setObjectName("Email")
#         self.txtfname = QtWidgets.QLineEdit(self.centralwidget)
#         self.txtfname.setGeometry(QtCore.QRect(230, 110, 371, 41))
#         self.txtfname.setObjectName("txtfname")
#         self.txtmail = QtWidgets.QLineEdit(self.centralwidget)
#         self.txtmail.setGeometry(QtCore.QRect(230, 270, 371, 41))
#         self.txtmail.setObjectName("txtmail")
#         self.txtlname = QtWidgets.QLineEdit(self.centralwidget)
#         self.txtlname.setGeometry(QtCore.QRect(230, 190, 371, 41))
#         self.txtlname.setObjectName("txtlname")
#         self.pushButton = QtWidgets.QPushButton(self.centralwidget)
#         self.pushButton.setGeometry(QtCore.QRect(320, 350, 151, 51))
#         self.pushButton.setStyleSheet("background-color: rgb(85, 85, 255);")
#         self.pushButton.setObjectName("pushButton")
#         MainWindow.setCentralWidget(self.centralwidget)

#         self.retranslateUi(MainWindow)
#         QtCore.QMetaObject.connectSlotsByName(MainWindow)

#     def retranslateUi(self, MainWindow):
#         _translate = QtCore.QCoreApplication.translate
#         MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#         self.Heading.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; font-style:italic; color:#ffffff;\">FORM 1</span></p></body></html>"))
#         self.Fname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">First Name</span></p></body></html>"))
#         self.Lname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">Last Name</span></p></body></html>"))
#         self.Email.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">Email</span></p></body></html>"))
#         self.pushButton.setText(_translate("MainWindow", "Submitt"))


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
