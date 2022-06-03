from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QDialog, QTableWidgetItem

from logWindow import log_Dialog
from mainGUI import Ui_MainWindow
from newOrden import Add_Dialog
from crearOrden import New_Dialog
from menuAdd import Menu_Dialog
import mysql.connector as mc

import sys


class SushiSystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # self.toolButton_add.clicked.connect(self.add_orden)
        self.toolButton_add.clicked.connect(self.add_orden)
        # self.toolButton_list.clicked.connect(self.select_data_hist)
        self.toolButton_list.clicked.connect(self.select_data_ord)
        self.toolButton_list_3.clicked.connect(self.select_data_hist)
        self.toolButton_list_3.clicked.connect(self.get_total)
        self.toolButton_list_2.clicked.connect(self.get_menu)
        self.actionnueva_sesion.triggered.connect(self.login)
        self.actionnueva_sesion.triggered.connect(self.get_name)
        # self.actionnueva_sesion.triggered.connect(self.get_name)
        self.actioncerrar_sesion.triggered.connect(self.logout)
        self.toolButton_add_menu.clicked.connect(self.add_Menu)
        self.toolButton_list_inv.clicked.connect(self.get_inv)

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
                self.label_user.setText(user)
                self.label_user_2.setText(user)
                self.label_user_3.setText(user)
                self.label_user_4.setText(user)
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

    def add_Menu(self):
        dialog = QDialog()
        ui = Menu_Dialog()
        ui.setupUi(dialog)
        ui.setupUi(dialog)
        user = self.get_name()
        ui.label_user.setText(str(user))

        dialog.exec()

    def logout(self):
        dbconfig = {
            'user': 'root',
            'password': 'admin123',
            'host': '127.0.0.1',
            'database': 'hikaru'
        }
        try:
            user = self.label_user.text()
            print(user)
            mydb = mc.connect(**dbconfig)
            mycursor = mydb.cursor()
            query = "UPDATE hikaru.users SET is_log = 'off' WHERE username = '" + user + "'"

            mycursor.execute(query)
            mydb.commit()
            self.label_user.setText("No hay usuario")
            self.label_user_2.setText("No hay usuario")
            self.label_user_3.setText("No hay usuario")
            self.label_user_4.setText("No hay usuario")

        except mc.Error as e:
            print(e)

    def select_data_ord(self):
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
                user = self.label_user.text()

                query = "SELECT id_orden, datetime, n_mesa, estado from ordenes where username like '" + user + "' and estado like 0 ORDER BY id_orden DESC"

                mycursor.execute(query)
                result = mycursor.fetchall()
                self.tableWidget_orden.setRowCount(len(result))
                self.tableWidget_orden.verticalHeader().setVisible(False)
                for row_number, row_data in enumerate(result):
                    print(row_number)
                    for column_number, data in enumerate(row_data):
                        print(column_number)
                        self.tableWidget_orden.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            except mc.Error as e:
                print(e)
        else:
            print(loged)
            print("not loged")


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
                user = self.label_user.text()

                query = "SELECT id_orden, username, datetime, n_mesa, total, estado from ordenes ORDER BY id_orden DESC "

                mycursor.execute(query)
                result = mycursor.fetchall()
                self.tableWidget_hist.setRowCount(len(result))
                self.tableWidget_hist.verticalHeader().setVisible(False)
                for row_number, row_data in enumerate(result):
                    print(row_number)
                    for column_number, data in enumerate(row_data):
                        print(column_number)
                        self.tableWidget_hist.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            except mc.Error as e:
                print(e)
        else:
            print(loged)
            print("not loged")

    def get_total(self):
        total = 0
        loged = self.is_log()
        if loged == 'on':
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
                query = "SELECT total FROM ordenes"
                mycursor.execute(query)
                result = mycursor.fetchall()
                for index in range(len(result)):
                    if result[index][0] == None:
                        loged = "off"

                    else:
                        total = total + result[index][0]
                        print(result[index][0])

                self.label_ventas.setText("            $" + str(total))
            except mc.Error as e:
                print(e)
        else:
            print("no hay sesion")
        return total

    def get_inv(self):
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
                query = "SELECT * FROM inventario"
                mycursor.execute(query)
                result = mycursor.fetchall()
                self.tableWidget_inv.setRowCount(len(result))
                self.tableWidget_inv.verticalHeader().setVisible(False)
                for row_number, row_data in enumerate(result):
                    print(row_number)
                    for column_number, data in enumerate(row_data):
                        print(column_number)
                        self.tableWidget_inv.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            except mc.Error as e:
                print(e)
        else:
            print("no hay sesion")


    def get_menu(self):
        loged = self.is_log()
        if loged == 'on':
            total = 0
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
                query = "SELECT nombre, descr, precio FROM menu"
                mycursor.execute(query)
                result = mycursor.fetchall()
                self.tableWidget_menu.setRowCount(len(result))
                self.tableWidget_menu.verticalHeader().setVisible(False)
                for row_number, row_data in enumerate(result):
                    print(row_number)
                    for column_number, data in enumerate(row_data):
                        print(column_number)
                        self.tableWidget_menu.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            except mc.Error as e:
                print(e)
            return total

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
