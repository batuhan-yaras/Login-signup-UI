import sys
import sqlite3
from PyQt5 import QtWidgets

class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.make_connection()
        self.init_ui()

    def make_connection(self):
        self.conn = sqlite3.connect("database.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Users (username TEXT,password TEXT)")

        self.conn.commit()


    def init_ui(self):
        self.usr = QtWidgets.QLabel("Username")
        self.username = QtWidgets.QLineEdit()
        self.psw = QtWidgets.QLabel("Password")
        self.password = QtWidgets.QLineEdit()
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.log_in = QtWidgets.QPushButton("Login")
        self.sign_up = QtWidgets.QPushButton("Sign Up")
        self.textplace = QtWidgets.QLabel("")


        v_box = QtWidgets.QVBoxLayout()
        v_box.addStretch()
        v_box.addWidget(self.usr)
        v_box.addWidget(self.username)
        v_box.addWidget(self.psw)
        v_box.addWidget(self.password)
        v_box.addWidget(self.textplace)
        v_box.addWidget(self.log_in)
        v_box.addWidget(self.sign_up)
        v_box.addStretch()

        h_box = QtWidgets.QHBoxLayout()
        h_box.addStretch()
        h_box.addLayout(v_box)
        h_box.addStretch()

        self.setLayout(h_box)
        self.setWindowTitle("Login-Sign up Interface")

        self.log_in.clicked.connect(self.login)
        self.sign_up.clicked.connect(self.signup)
        self.setGeometry(700,300,300,300)
        self.show()

    def login(self):
        name = self.username.text()
        pas = self.password.text()

        self.cursor.execute("SELECT * FROM Users WHERE username = ? and password = ?",(name,pas))
        data = self.cursor.fetchall()

        if len(data) == 0:
            self.textplace.setText("Username or password is wrong.\nPlease try again.")
        else:
            self.textplace.setText("Welcome "+name)

    def signup(self):
        conn = sqlite3.connect("database.db")
        self.cursor = conn.cursor()
        name = self.username.text()
        pas = self.password.text()

        self.cursor.execute("SELECT username FROM Users WHERE username = ?",(name,))
        data = self.cursor.fetchall()
        if len(data) == 0:
            if len(name) >= 5:
                self.cursor.execute("Insert into Users VALUES (?,?)", (name, pas))
                self.textplace.setText("Succesfully signed up!")
                conn.commit()
            else:
                self.textplace.setText("Your username is too short\nAt least 4 character needed.")
        else:
            self.textplace.setText("There is already a user with this username!")


app = QtWidgets.QApplication(sys.argv)
interface = Interface()
sys.exit(app.exec_())