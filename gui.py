# from DataBase import DataBase
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog

import sys

import logging
logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("main.ui", self)

    def open_auth(self, w):
        dialog = DialogAuth(self, w)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()


class DialogAuth(QDialog):
    def __init__(self, w, parent=None):
        self.w = w
        super(DialogAuth, self).__init__(parent)
        self.ui = uic.loadUi("auth.ui", self)
        self.ui.btn_enter.clicked.connect(self.enter)

    def enter(self):
        """
        сюда надо вернуть
        :return:
        """

        auth_log = self.login.text()
        auth_pas = self.password.text()

        if auth_log == '' or auth_pas == '':
            logging.log(logging.INFO, 'Ошибка. Введите логин и пароль')

        if auth_log != '' and auth_pas != '':
            # вернуть из бд пароль и роль по логину, если такого логина нет, тогда вернуть '', '' (2 пустых строки)
            password, role = '1', 'администратор'

            if password != self.password.text():
                logging.log(logging.INFO, 'Ошибка')

            elif password == self.password.text():
                logging.log(logging.INFO, 'Вход выполнен')
                if role == 'Старший смены':
                    self.w.hide()
                elif role == 'Продавец':
                    self.w.hide()
                else:
                    self.w.hide()

                self.w.show()
                self.close()

class Builder:
    def __init__(self):
        self.qapp = QApplication(sys.argv)
        self.window = MainWindow()
        self.auth()

    def auth(self):
        self.window.open_auth(self.window)
        self.qapp.exec()


if __name__ == '__main__':
    B = Builder()
