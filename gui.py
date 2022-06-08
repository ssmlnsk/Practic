# from DataBase import DataBase
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog

import sys
import time

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
        self.visible_captcha(False)
        self.count_try_entry = 0
        self.now_captcha = None
        self.next_try = 0

    def create_captcha(self):
        pass

    def visible_captcha(self, visible=True):
        self.ui.draw_captcha.setVisible(visible)
        self.ui.edit_captcha.setVisible(visible)
        self.ui.label_4.setVisible(visible)
        self.ui.btn_new_captcha.setVisible(visible)

    def captcha_generation(self):
        return
        pass

    def enter(self):
        """
        при нажатии на кнопку вход
        """
        t = time.localtime()
        now_time = time.mktime(t)  # переводим в секунды
        auth_log = self.ui.edit_login.text()
        auth_pas = self.ui.edit_password.text()

        if auth_log == '' or auth_pas == '':
            logging.log(logging.INFO, 'Ошибка. Заполните все поля!')
        elif self.now_captcha is not None and self.ui.edit_captcha.text() == '':    # если капча существует и она не пустая
            logging.log(logging.INFO, 'Ошибка. Введите капчу!')
        else:
            """ вернуть из бд пароль, роль, последний выход и блокировку (true, false) по логину, если такого логина нет, тогда вернуть '', '', '', '' (4 пустых строки) """
            password, role, last_exit, block = '1', 'администратор', '09:06:2022 00:49:00', True   # временные данные (сюда надо возвращать из бд)
            if last_exit is not None and block:     # после окончания предыдущей сессии, новую можно начать только через 3 минуты
                last_exit = last_exit.split()
                day, mon, year = map(int, last_exit[0].split(':'))
                hour, mi, sec = map(int, last_exit[1].split(':'))
                time_block = time.mktime((year, mon, day, hour, mi+3, sec, 0, 0, 0))    # переводим в секунды с учетом 3х минут блокировки
                if time_block > now_time:
                    logging.log(logging.INFO, 'Ошибка. Подождите, время нового сеанса еще не пришло.')
                    return

            if self.count_try_entry >= 3 and self.next_try > now_time:    # не прошло 10 секунд с прошлой попытки входа (после 3 неуспешной попытки)
                logging.log(logging.INFO, 'Ошибка. Подождите, прежде чем пытаться вводить снова')
                return

            if self.now_captcha is not None and self.now_captcha != self.ui.edit_captcha.text():
                logging.log(logging.INFO, 'Ошибка. Неправильно введена капча')
            elif password != auth_pas:    # неправильный пароль или вернул пустую строку тк нет такого логина
                self.count_try_entry += 1
                if self.count_try_entry >= 3:
                    self.next_try = now_time+10
                time_error_entry = time.strftime("%d:%m:%Y %H:%M:%S", t)    # время неуспешной попытки входа
                # print(time_error_entry)
                """
                time_error_entry Для Паши в историю входа (неуспешный вход)
                """
                if self.count_try_entry == 2:
                    self.visible_captcha(True)
                    self.now_captcha = self.captcha_generation()
                    logging.log(logging.INFO, 'Ошибка. Вторая неуспешная попытка входа. Теперь введите капчу.')
                else:
                    logging.log(logging.INFO, 'Ошибка. Неправильно введены данные')
            elif password == self.ui.password.text():
                time_success_entry = time.strftime("%d:%m:%Y %H:%M:%S", t)    # время успешной попытки входа
                """
                time_success_entry Для Паши в историю входа (успешный вход) и для последнего входа сотрудника (в employeers)
                """
                logging.log(logging.INFO, 'Вход выполнен')
                print(time.time())
                if role == 'Старший смены':
                    self.w.hide()
                elif role == 'Продавец':
                    self.w.hide()
                else:
                    self.w.hide()
                self.w.show()
                self.close()

        if self.count_try_entry == 2:
            self.count_try_entry += 1   # чтобы сюда больше не заходил
            self.visible_captcha(True)
            self.now_captcha = self.captcha_generation()

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
