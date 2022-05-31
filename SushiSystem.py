from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem
from mainGuiDemo import Ui_MainWindow
from newOrden import Add_Dialog
from crearOrden import New_Dialog
import mysql.connector as mc
from logWimdow import log_Dialog

import sys


class SushiSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.toolButton_add.clicked.connect(self.add_orden)
        self.toolButton_add.clicked.connect(self.add_orden)
        self.toolButton_list.clicked.connect(self.select_data_hist)
        self.actionnueva_sesion.triggered.connect(self.login)
        self.actionnueva_sesion.triggered.connect(self.get_name)
        self.actioncerrar_sesion.triggered.connect(self.logout)


    def get_name(self):
        user = "no hay sesion"
        try:
            dbconfig = {
                'user': 'root',
                'password': 'admin123',
                'host': '127.0.0.1',
                'database': 'hikaru'
            }
            mydb = mc.connect(**dbconfig)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT username FROM users WHERE is_log = 'on'")
            result = mycursor.fetchone()
            if result != None:
             user = result[0]
             self.label_6.setText(user)
            else:
                print("inicia sesion")


        except mc.Error as e:
            print(e)
        return user


    def add_orden(self):
        loged = self.is_log()
        if loged == 'on':
            dialog = QDialog()
            ui = New_Dialog()
            ui.setupUi(dialog)
            user = self.get_name()
            ui.label_user.setText(str(user))

            dialog.exec()
        elif loged == 'off':
            print(loged)
            print("not loged")


    def login(self):
        dialog = QDialog()
        ui = log_Dialog()
        ui.setupUi(dialog)


        dialog.exec()


    def logout(self):
        dbconfig = {
            'user': 'root',
            'password': 'admin123',
            'host': '127.0.0.1',
            'database': 'hikaru'
        }
        try:
            user = self.label_6.text()
            print(user)
            mydb = mc.connect(**dbconfig)
            mycursor = mydb.cursor()
            query = "UPDATE hikaru.users SET is_log = 'off' WHERE username = '" + user + "'"

            mycursor.execute(query)
            mydb.commit()
            self.label_6.setText("No hay usuario")

        except mc.Error as e:
            print(e)


    def select_data_hist(self):
        loged = self.is_log()
        if loged == 'on':
            try:
                dbconfig = {
                    'user': 'root',
                    'password': 'admin123',
                    'host': '127.0.0.1',
                    'database': 'hikaru'
                }
                mydb = mc.connect(**dbconfig)
                mycursor = mydb.cursor()
                user = self.label_6.text()

                query = "SELECT id_orden, username, datetime, n_mesa,total,estado from ordenes where username like '" + user + "' and estado like 0"

                mycursor.execute(query)
                result = mycursor.fetchall()
                self.tableWidget_2.setRowCount(len(result))
                for row_number, row_data in enumerate(result):
                    print(row_number)
                    for column_number, data in enumerate(row_data):
                        print(column_number)
                        self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(data)))

                row = self.tableWidget_2.item(0, 2).text()
                print(row)

            except mc.Error as e:
                print(e)
        else:
            print(loged)
            print("not loged")


    def is_log(self):
        try:
            dbconfig = {
                'user': 'root',
                'password': 'admin123',
                'host': '127.0.0.1',
                'database': 'hikaru'
            }
            user = self.get_name()
            mydb = mc.connect(**dbconfig)
            mycursor = mydb.cursor()
            query = "SELECT is_log FROM users WHERE username like '" + user + "'"
            mycursor.execute(query)
            result = mycursor.fetchone()
            if result == None:
                loged = "off"

            else:
                loged = result[0]
                print(result[0])
        except mc.Error as e:
            print(e)
        return loged
