# Form implementation generated from reading ui file 'menuSelect.ui'
#
# Created by: PyQt6 UI code generator 6.1.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
import mysql.connector as mc
from PyQt6.QtWidgets import QListWidgetItem


class menuSc_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(407, 300)
        self.list_menu_selec = QtWidgets.QListWidget(Dialog)
        self.list_menu_selec.setGeometry(QtCore.QRect(15, 71, 371, 161))
        self.list_menu_selec.setObjectName("list_menu_selec")
        self.pushButton__act = QtWidgets.QPushButton(Dialog)
        self.pushButton__act.setGeometry(QtCore.QRect(80, 250, 251, 31))
        self.pushButton__act.setObjectName("pushButton__act")
        self.line_se_menu = QtWidgets.QLineEdit(Dialog)
        self.line_se_menu.setGeometry(QtCore.QRect(20, 20, 321, 31))
        self.line_se_menu.setObjectName("line_se_menu")
        self.pushButton_search = QtWidgets.QPushButton(Dialog)
        self.pushButton_search.setGeometry(QtCore.QRect(350, 20, 41, 31))
        self.pushButton_search.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/images/search-50.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton_search.setIcon(icon)
        self.pushButton_search.setObjectName("pushButton_search")
        self.pushButton_search.clicked.connect(self.menu_select)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def menu_select(self):
        try:
            dbconfig = {
                'user': 'root',
                'password': 'admin123',
                'host': '127.0.0.1',
                'database': 'hikaru'
            }
            nom = self.line_se_menu.text()
            mydb = mc.connect(**dbconfig)
            mycursor = mydb.cursor()
            if nom == "":
                print("no hay nada escrito")
            else:
                query = "SELECT nombre from menu where nombre like '%" + nom + "%'"

                mycursor.execute(query)
                result = mycursor.fetchall()
                if len(result) > 0:
                    i = 0
                    while i < len(result):
                        men = result[i][0]
                        print(men)
                        self.list_menu_selec.addItem(result[i][0])
                        print(i, "asd")
                        i += 1
                else:
                    self.list_menu_selec.addItem("no hay en el menu")
        except mc.Error as e:
            print(e)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Menu"))
        self.pushButton__act.setText(_translate("Dialog", "aceptar"))
