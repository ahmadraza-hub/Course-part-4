from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(763, 365)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Background = QtWidgets.QLabel(self.centralwidget)
        self.Background.setGeometry(QtCore.QRect(-280, -170, 1601, 861))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.Background.setFont(font)
        self.Background.setStyleSheet("background-color: rgb(170, 170, 0);")
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
        self.txtfname = QtWidgets.QLineEdit(self.centralwidget)
        self.txtfname.setGeometry(QtCore.QRect(230, 110, 371, 41))
        self.txtfname.setObjectName("txtfname")
        self.txtlname = QtWidgets.QLineEdit(self.centralwidget)
        self.txtlname.setGeometry(QtCore.QRect(230, 190, 371, 41))
        self.txtlname.setObjectName("txtlname")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(320, 280, 151, 51))
        self.pushButton.setStyleSheet("background-color: rgb(170, 85, 127);")
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Heading.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; font-style:italic; color:#ffffff;\">Login Page</span></p></body></html>"))
        self.Fname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">username</span></p></body></html>"))
        self.Lname.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-style:italic; color:#ffffff;\">password</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "login"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
