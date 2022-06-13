from io import BytesIO

import barcode
from barcode import EAN13
from barcode.writer import ImageWriter
import img2pdf

from facade import Facade
import random

from PyQt5.QtGui import QFont, QPixmap
from PyQt5 import QtWidgets
from PyQt5 import uic, QtCore, QtGui
from PyQt5.QtCore import Qt, QTimer, QTime, QDateTime
from PyQt5.QtWidgets import QGraphicsScene, QListWidgetItem
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem, QDialog

import sys
import time
import datetime

import logging

from PyQt5.QtWidgets import QMessageBox

logging.basicConfig(level=logging.INFO)


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Отвечает за подключением к кнопкам, объявление переменных, заполнение таблиц,
        получение списка страниц StackedWidget
        """
        super().__init__()
        self.facade = Facade()
        self.ui = uic.loadUi("main.ui", self)
        self.page = self.ui.stackedWidget_main
        self.page_id = [0]  # тут будут индексы доступных страничек после авторизации для сотрудника
        self.now_page = 0

        self.time = QtCore.QTime(0, 10, 0)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Counter)

        self.page.setCurrentIndex(self.page_id[self.now_page])
        self.ui.btn_next.clicked.connect(self.next_page)
        self.ui.btn_back.clicked.connect(self.back_page)
        self.ui.btn_all_clients.clicked.connect(self.page_all_clients)
        self.ui.btn_exit.clicked.connect(lambda: self.exit(False))

        self.ui.btn_new_serv.clicked.connect(self.new_service)
        self.ui.btn_delete_serv.clicked.connect(self.delete_service)
        self.ui.btn_save_serv.clicked.connect(self.save_service)

        self.build_combobox_clients()
        self.build_combobox_services()

        self.ui.btn_new_order.clicked.connect(self.add_new_request)
        self.ui.btn_save_request.clicked.connect(self.save_request)
        self.ui.btn_plus.clicked.connect(self.add_service_to_request)
        self.ui.btn_code.clicked.connect(self.generateCode)

        self.ui.btn_new_client.clicked.connect(self.oped_new_client)

        self.ui.btn_count_order.clicked.connect(self.count_order)
        self.ui.btn_count_serv.clicked.connect(self.count_serv)
        self.ui.btn_count_order_serv.clicked.connect(self.count_order_serv)

        self.type = 0
        self.dict = {}
        if self.ui.btn_count_order.clicked:
            self.type = 1
        elif self.ui.btn_count_order_serv.clicked:
            self.type = 3
        elif self.ui.btn_count_serv.clicked:
            self.type = 2

        self.ui.btn_pdf.clicked.connect(lambda: self.order_pdf(self.type, self.dict))

        self.updateTableServ()
        self.updateTableHistory()

    def Counter(self):
        """
        ???
        :return:
        """
        self.time = self.time.addSecs(-1)
        self.lcdTimer.display(self.time.toString("hh:mm:ss"))
        if self.time == QTime(0, 2, 0):
            self.messagebox = QMessageBox(self)
            self.messagebox.setWindowTitle("Внимание!")
            self.messagebox.setText("До завершения сеанса осталось 2 минуты!")
            self.messagebox.setStandardButtons(QMessageBox.Ok)
            self.messagebox.show()

        if self.time == QTime(0, 0, 0):
            self.window().exit(False)
            self.timer.stop()

    def exit(self, block):
        """
        Отвечает за выход из программы
        :param block: блокировка
        :return:
        """
        self.now_page = 0
        self.page.setCurrentIndex(self.page_id[self.now_page])
        t = time.localtime()
        time_string = time.strftime("%d:%m:%Y %H:%M:%S", t)  # время выхода
        self.facade.insert_time_exit(self.now_login, time_string, block)
        self.hide()
        self.open_auth()

    def page_all_clients(self):
        """
        Отвечает за переход к странице с таблицей клиентов
        Обновление таблицы клиентов
        :return:
        """
        self.toTable()
        self.page.setCurrentIndex(3)

    def toTable(self):
        """
        Отвечает за обновление таблицы клиентов
        :return:
        """
        self.table_serv.clear()
        rec = self.facade.read_clients()
        self.ui.table_clients.setColumnCount(7)
        self.ui.table_clients.setRowCount(len(rec))
        self.ui.table_clients.setHorizontalHeaderLabels(['ФИО', 'Код клиента', 'Паспротные данные', 'Дата рождения', 'Адрес', 'e-mail', 'password'])

        for i, client in enumerate(rec):
            for x, field in enumerate(client):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_clients.setItem(i, x, item)

    def updateTableServ(self):
        """
        Отвечает за обновление таблицы услуг
        :return:
        """
        self.table_serv.clear()
        rec = self.facade.read_services()
        self.ui.table_serv.setColumnCount(4)
        self.ui.table_serv.setRowCount(len(rec))
        self.ui.table_serv.setHorizontalHeaderLabels(['ID', 'Название услуги', 'Код услуги', 'Стоимость руб. за час'])

        for i, service in enumerate(rec):
            for x, field in enumerate(service):
                item = QTableWidgetItem()
                item.setText(str(field))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_serv.setItem(i, x, item)

    def updateTableHistory(self):
        """
        Отвечает за обновление таблицы истории входа
        :return:
        """
        self.table_entry.clear()
        rec = self.facade.read_history()
        self.table_entry.setColumnCount(5)
        self.table_entry.setRowCount(len(rec))
        self.table_entry.setHorizontalHeaderLabels(['ID', 'Дата входа', 'Дата выхода', 'Блокировка', 'Логин сотрудника'])

        for i, employee in enumerate(rec):
            for x, info in enumerate(employee):
                item = QTableWidgetItem()
                item.setText(str(info))
                if x == 0:
                    item.setFlags(Qt.ItemIsEnabled)
                self.ui.table_entry.setItem(i, x, item)

    def new_service(self):
        """
        Отвечает за добавление новой услуги
        :return:
        """
        title_serv = self.ui.edit_title_serv.text()
        code_serv = self.ui.edit_code_serv.text()
        cost_serv = self.ui.spin_cost.value()
        if title_serv != '' and code_serv != '' and cost_serv != '':
            self.facade.insert_service(title_serv, code_serv, cost_serv)
            self.updateTableServ()

    def delete_service(self):
        """
        Отвечает за удаление выбранной услуги
        :return:
        """
        SelectedRow = self.table_serv.currentRow()
        rowcount = self.table_serv.rowCount()
        colcount = self.table_serv.columnCount()

        if rowcount == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("В таблице нет данных!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        elif SelectedRow == -1:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Выберите поле для удаления!")
            msg.setWindowTitle("Ошибка")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

        else:
            for col in range(1, colcount):
                self.table_serv.setItem(SelectedRow, col, QTableWidgetItem(''))
            ix = self.table_serv.model().index(-1, -1)
            self.table_serv.setCurrentIndex(ix)

    def get_from_table(self):
        """
        Получение данных из таблицы, чтобы потом записать их в БД
        :return: data
        """
        rows = self.table_serv.rowCount()
        cols = self.table_serv.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(cols):
                tmp.append(self.table_serv.item(row, col).text())
            data.append(tmp)
        return data

    def save_service(self):
        """
        Отвечает за сохранение данных об услугах в базу данных
        Обновление таблицы в интерфейсе
        :return:
        """
        data = self.get_from_table()
        for string in data:
            if string[1] != '':  # если название услуги есть, то обновляем данные
                self.facade.update_service(int(string[0]), string[1], string[2], string[3])
            else:  # если названия услуги нет, то удаляем эту строку
                self.facade.delete_service(int(string[0]))
        self.updateTableServ()

    def build_combobox_clients(self):
        """
        Добавление списка клиентов в ComboBox
        :return:
        """
        clients = self.facade.get_clients()
        self.comboBox_clients.clear()
        if self.comboBox_clients is not None:
            self.comboBox_clients.addItems(clients)
        logging.log(logging.INFO, 'ComboBox "Клиенты" обновлён')

    def build_combobox_services(self):
        """
        Добавление списка услуг в ComboBox
        :return:
        """
        services = self.facade.get_services()
        self.comboBox_serv.clear()
        if self.comboBox_serv is not None:
            self.comboBox_serv.addItems(services)
        logging.log(logging.INFO, 'ComboBox "Услуги" обновлён')

    def add_new_request(self):
        """
        Оформление нового заказа и его показ в ListWidget
        :return:
        """
        self.number = QListWidgetItem(str(self.spin_num_order.value()))
        self.number_title = QListWidgetItem("Номер заказа:")
        self.client = QListWidgetItem(self.comboBox_clients.currentText())
        self.client_code = QListWidgetItem(self.facade.get_code_client(self.comboBox_clients.currentText()))
        self.client_title = QListWidgetItem("Клиент:")
        self.service = QListWidgetItem(self.comboBox_serv.currentText())
        self.service_title = QListWidgetItem("Услуга:")
        self.datetime = datetime.datetime.now()
        self.date_req_title = QListWidgetItem("Дата создания:")
        self.date_req = str(self.datetime.strftime("%d.%m.%Y"))
        self.time_req_title = QListWidgetItem("Время заказа:")
        self.time_req = str(self.datetime.strftime("%H:%M"))
        self.add_new_field.clear()
        if self.number != '' and self.client != '' and self.service != '':
            self.add_new_field.addItem(self.number_title)
            self.add_new_field.addItem(self.number)
            self.add_new_field.addItem(self.date_req_title)
            self.add_new_field.addItem(self.date_req)
            self.add_new_field.addItem(self.time_req_title)
            self.add_new_field.addItem(self.time_req)
            self.add_new_field.addItem(self.client_title)
            self.add_new_field.addItem(self.client_code)
            self.add_new_field.addItem(self.client)
            self.add_new_field.addItem(self.service_title)
            self.add_new_field.addItem(self.service)

    def add_service_to_request(self):
        """
        Добавление услуги в заказ
        :return:
        """
        self.service = QListWidgetItem(self.comboBox_serv.currentText())
        self.add_new_field.addItem(self.service)

    def save_request(self):
        """
        Отвечает за сохранение заказа в базу данных
        :return:
        """
        ignore_serv = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        ignore2 = [1, 3, 5, 7]
        count = self.add_new_field.count()
        list_serv = [ind for ind in range(count) if ind not in ignore_serv]
        list_req = [ind for ind in range(count) if ind in ignore2]
        request = []
        serv = []
        for i in list_serv:
            name = self.add_new_field.item(i).text()
            id_serv = self.facade.get_id_serv(name)
            serv.append(id_serv)
            list_serv_for_request = str(serv).replace("'", "")

        for j in list_req:
            if j == 7:
                fio = str(self.add_new_field.item(j).text())
                id_client = self.facade.get_id_client(fio)
                request.append(id_client)
            else:
                request.append(self.add_new_field.item(j).text())

        number = str(request[0] + "/" + request[1])

        self.facade.create_request(number, request[1], request[2], request[3], list_serv_for_request[1:-1])
        self.updateTableServ()

    def generateCode(self):
        """
        Отвечает за создание штрих-кода по номеру, дате и времени заказа
        Создаётся в форматах .png и .pdf
        :return:
        """
        rv = BytesIO()
        EAN13 = barcode.get_barcode_class('code39')
        EAN13(str(100000902922), writer=ImageWriter()).write(rv)

        temp = str(self.spin_num_order.value()) + str(self.date_req) + str(self.time_req)
        temp_middle = temp.replace(".", "")
        temp_end = temp_middle.replace(":", "")

        name = "code" + temp_end

        with open("codes/" + name + '.png', "wb") as f:
            EAN13(temp_end, writer=ImageWriter(), add_checksum=False).write(f)

        a4_page_size = [img2pdf.in_to_pt(8.3), img2pdf.in_to_pt(11.7)]
        layout_function = img2pdf.get_layout_fun(a4_page_size)

        pdf = img2pdf.convert("codes/" + name + '.png', layout_fun=layout_function)
        with open("codes/" + name + '.pdf', 'wb') as f:
            f.write(pdf)

        icon = QtGui.QIcon('codes/' + name + '.png')
        item = QtWidgets.QListWidgetItem(icon, "")
        self.add_new_field.addItem(item)

        self.mes_box('Штрих-код создан.')

    def mes_box(self, text):
        """
        Открывает messagebox с переданным текстом.
        Вызывается при успешном создании кода.
        :param text: текст для вывода в messagebox
        """
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Штрих-код")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

    def otchot(self):
        start = self.date_start.dateTime().toString('yyyy.MM.dd')
        end = self.date_end.dateTime().toString('yyyy.MM.dd')
        data = list(self.facade.get_date_serv())
        count_serv = {}  # 1
        count_order_serv = {}  # 2
        count_order = {}  # 3

        for i, date in enumerate(data):
            data[i] = list(data[i])
            d = date[1].split('.')
            data[i][1] = d[2] + '.' + d[1] + '.' + d[0]
            if data[i][1] >= start and data[i][1] <= end:
                servs = date[0].split()
                try:
                    count_order[date[1]] += 1
                except KeyError:
                    count_order[date[1]] = 1
                try:
                    count_serv[date[1]] += len(servs)
                except:
                    count_serv[date[1]] = len(servs)
                try:
                    count_order_serv[date[1]]
                except KeyError:
                    count_order_serv[date[1]] = {}

                for s in servs:
                    try:
                        count_order_serv[date[1]][s] += 1
                    except KeyError:
                        count_order_serv[date[1]][s] = 1
        return [count_order, count_serv, count_order_serv]

    def count_order(self):
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchot()
        rec = temp[0]
        self.dict = temp[0]
        self.table_graf.setColumnCount(2)
        self.table_graf.setRowCount(len(rec))
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Количество заказов'])

        data = []
        count = []

        for d, c in rec.items():
            data.append(d)
            count.append(c)

        for row, value1 in enumerate(data):
            item = QTableWidgetItem()
            item.setText(str(value1))
            self.table_graf.setItem(row, 0, item)

        for row, value2 in enumerate(count):
            item = QTableWidgetItem()
            item.setText(str(value2))
            self.table_graf.setItem(row, 1, item)

    def count_serv(self):
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchot()
        rec = temp[1]
        self.dict = temp[1]
        self.table_graf.setColumnCount(2)
        self.table_graf.setRowCount(len(rec))
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Количество услуг'])

        data = []
        count = []

        for d, c in rec.items():
            data.append(d)
            count.append(c)

        for row, value1 in enumerate(data):
            item = QTableWidgetItem()
            item.setText(str(value1))
            self.table_graf.setItem(row, 0, item)

        for row, value2 in enumerate(count):
            item = QTableWidgetItem()
            item.setText(str(value2))
            self.table_graf.setItem(row, 1, item)

    def count_order_serv(self):
        self.table_graf.setRowCount(0)
        self.table_graf.setColumnCount(0)
        temp = self.otchot()
        rec = temp[2]
        self.dict = temp[2]
        day = []
        serv = []
        count = []
        lenght = 0

        for d in rec.items():
            for i in d:
                if i == d[1]:
                    temp = []
                    temp2 = []
                    for j in i:
                        temp.append(j)
                    serv.append(temp)
                    for k in i:
                        temp2.append(i[k])
                    count.append(temp2)
                else:
                    day.append(i)

        for i in serv:
            lenght += len(i)

        x = 0
        x2 = 0

        self.table_graf.setRowCount(lenght)
        self.table_graf.setColumnCount(3)
        self.table_graf.setHorizontalHeaderLabels(['Дата', 'Услуги', 'Количество услуг'])

        for row, value1 in enumerate(day):
            temp_serv = serv[row]
            temp_count = count[row]
            len_serv = len(temp_serv)
            self.table_graf.setSpan(x, 0, len_serv, 1)
            item = QTableWidgetItem(str(value1))
            self.table_graf.setItem(x, 0, item)
            for i in temp_serv:
                item_serv = QTableWidgetItem(i)
                self.table_graf.setItem(x, 1, item_serv)
                x += 1
            for j in temp_count:
                item_count = QTableWidgetItem(str(j))
                self.table_graf.setItem(x2, 2, item_count)
                x2 += 1

    def order_pdf(self, type, data):
        from fpdf import FPDF
        x, y = 10, 60
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('Calibri Regular', '', 'C:\Windows\Fonts\calibri.ttf', uni=True)
        pdf.set_font('Calibri Regular', size=25)
        pdf.image('img/logo.png', w=30, h=30)

        if type == 1:
            pdf.cell(200, -30, txt="Отчёт по кол-ву оказанных услуг по дням", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Кол-во оказанных услуг')
            for d in data:
                y += 10
                if y == 300:
                    y, x = 10, 10
                    pdf.add_page()
                    pdf.text(x, y, 'Дата')
                    pdf.text(x + 60, y, 'Кол-во оказанных услуг')
                    y += 10
                pdf.text(x, y, d)
                pdf.text(x + 60, y, str(data[d]))
            pdf.output("report_serv.pdf")

        elif type == 2:
            pdf.cell(200, -30, txt="Отчёт по кол-ву заказов по каждой услуге", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Номер услуги')
            pdf.text(x + 120, y, 'Кол-во оказанных услуг')
            for d in data:
                pdf.text(x, y + 10, d)
                for serv in data[d]:
                    y += 10
                    if y == 300:
                        y, x = 10, 10
                        pdf.add_page()
                        pdf.text(x, y, 'Дата')
                        pdf.text(x + 60, y, 'Номер услуги')
                        pdf.text(x + 120, y, 'Кол-во оказанных услуг')
                        y += 10
                    pdf.text(x + 63, y, str(y))
                    pdf.text(x + 123, y, str(data[d][serv]))
            pdf.output("report_order_serv.pdf")

        elif type == 3:
            pdf.cell(200, -30, txt="Отчёт по кол-ву заказов по дням", ln=1, align="C")
            pdf.set_font('Calibri Regular', size=14)
            pdf.text(x, y, 'Дата')
            pdf.text(x + 60, y, 'Кол-во заказов')
            for d in data:
                y += 10
                if y == 300:
                    y, x = 10, 10
                    pdf.add_page()
                    pdf.text(x, y, 'Дата')
                    pdf.text(x + 60, y, 'Кол-во заказов')
                    y += 10
                pdf.text(x, y, d)
                pdf.text(x + 60, y, str(data[d]))
            pdf.output("report_order.pdf")

    def next_page(self):
        """
        Отвечает за переход к следующей странице
        :return:
        """
        if self.now_page != len(self.page_id)-1:
            self.now_page += 1
            self.page.setCurrentIndex(self.page_id[self.now_page])

    def back_page(self):
        """
        Отвечает за переход к предыдущей странице
        :return:
        """
        if self.now_page != 0:
            self.now_page -= 1
            self.page.setCurrentIndex(self.page_id[self.now_page])

    def open_auth(self):
        """
        Создает и показывает диалоговое окно авторизации.
        Вызывается в __init__ и в функции exit
        :return:
        """
        dialog = DialogAuth(self)
        dialog.setWindowTitle("Авторизация")
        dialog.show()
        dialog.exec_()

    def oped_new_client(self):
        """
        Создает и показывает диалоговое окно создания нового клиента.
        :return:
        """
        dialog_client = DialogNewClient(self)
        dialog_client.setWindowTitle("Добавление нового клиента")
        dialog_client.show()
        dialog_client.exec_()


class DialogAuth(QDialog):
    def __init__(self, parent=None):
        """
        Отвечает за подключением к кнопкам, объявление переменных, создание сцены для «graphicsView»
        """
        super(DialogAuth, self).__init__(parent)
        self.ui = uic.loadUi("auth.ui", self)
        self.facade = Facade()

        self.scene = QGraphicsScene(0, 0, 300, 80)
        self.ui.draw_captcha.setScene(self.scene)
        self.ui.btn_enter.clicked.connect(self.enter)
        self.ui.btn_new_captcha.clicked.connect(self.captcha_generation)
        self.ui.btn_hide_password.clicked.connect(self.vis_pas)
        self.visible_captcha(False)

        self.count_try_entry = 0
        self.now_captcha = None
        self.next_try = 0
        self.vis_p = False

    def vis_pas(self):
        """
        Вызывается при нажатии на кнопку «btn_hide_password».
        Скрывает и показывает пароль (в соответствии с переменной self.vis_p)
        """
        ed = self.ui.edit_password
        if self.vis_p:
            self.vis_p = False
            ed.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.vis_p = True
            ed.setEchoMode(QtWidgets.QLineEdit.Normal)

    def visible_captcha(self, visible=True):
        """
        Вызывается в __init__ (с параметром False) и при второй неуспешной попытки входа
        (неправильный ввод пароля или логина) с параметом True.
        :param visible:
        При False скрывает поле ввода, кнопку обновления и сцену для отрисовки капчи
        При True - показывает поле ввода, кнопку обновления и сцену для отрисовки капчи
        """
        self.ui.draw_captcha.setVisible(visible)
        self.ui.edit_captcha.setVisible(visible)
        self.ui.label_4.setVisible(visible)
        self.ui.btn_new_captcha.setVisible(visible)

    def captcha_generation(self):
        """
        Вызывается при второй неуспешной попытке входа и при нажатии на кнопку «btn_new_captcha».
        Выводит капчу в «graphicsView» и возвращает значение капчи в переменной self.now_captcha
        """
        self.scene.clear()
        syms = 'qwertyuiopasdfghjklzxcvbnm1234567890'
        count_syms = 3
        now_syms = ['']*count_syms
        x, y = 30, 20

        self.scene.addLine(0, random.randint(20, 45), 200, random.randint(30, 60))

        for i in range(count_syms):
            now_syms[i] = syms[random.randint(0, 35)]
            x+=20
            text = self.scene.addText(f"{now_syms[i]}")
            text.setFont(QFont("MS Shell Dlg 2", 15))
            text.moveBy(x, y+random.randint(-10, 20))
        self.now_captcha = ''.join(now_syms)

    def mes_box(self, text):
        """
        Открывает messagebox с переданным текстом.
        Вызывается при неверном вводе пользователем логина, пароля, капчи.
        :param text: текст для вывода в messagebox
        """
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()

    def enter(self):
        """
        Вызывается при нажатии на кнопку btn_enter.
        Обрабатывает все случаи ввода данных (капчи, логина, пароля) и считает неуспешные попытки входа.
        Проверяет есть ли у пользователя блокировка и до скольки она длиться.
        При успешном входе передает в фасад время и логин успешного входа (для записи в бд),
        записывает индексы доступных страничек «Stacked Widget»
        (у разных сотрудников могут быть разные странички)
        """
        t = time.localtime()
        now_time = time.mktime(t)  # переводим в секунды
        auth_log = self.ui.edit_login.text()
        auth_pas = self.ui.edit_password.text()

        if auth_log == '' or auth_pas == '':
            logging.log(logging.INFO, 'Ошибка. Заполните все поля!')
            self.mes_box('Заполните все поля!')

        elif self.now_captcha is not None and self.ui.edit_captcha.text() == '':    # если капча существует и она не пустая
            logging.log(logging.INFO, 'Ошибка. Введите капчу!')
            self.mes_box('Введите капчу!')
        else:
            password, role, last_exit, block, fio, photo = self.parent().facade.get_for_authorization(auth_log)
            pix = QPixmap(f'img/{photo}')
            if last_exit is not None and block:     # после окончания предыдущей сессии, новую можно начать только через 3 минуты
                last_exit = last_exit.split()
                day, mon, year = map(int, last_exit[0].split(':'))
                hour, mi, sec = map(int, last_exit[1].split(':'))
                time_block = time.mktime((year, mon, day, hour, mi+3, sec, 0, 0, 0))    # переводим в секунды с учетом 3х минут блокировки
                if time_block > now_time:
                    logging.log(logging.INFO, 'Ошибка. Подождите, время нового сеанса еще не пришло.')
                    self.mes_box('Подождите, время нового сеанса еще не пришло.')
                    return

            if self.count_try_entry >= 3 and self.next_try > now_time:    # не прошло 10 секунд с прошлой попытки входа (после 3 неуспешной попытки)
                logging.log(logging.INFO, 'Ошибка. Подождите, прежде чем пытаться вводить снова.')
                self.mes_box('Подождите, прежде чем пытаться вводить снова.')
                return

            if self.now_captcha is not None and self.now_captcha != self.ui.edit_captcha.text():
                logging.log(logging.INFO, 'Ошибка. Неправильно введена капча.')
                self.mes_box('Неправильно введена капча.')
            elif password != auth_pas:    # неправильный пароль или вернул пустую строку тк нет такого логина
                self.count_try_entry += 1
                if self.count_try_entry >= 3:
                    self.next_try = now_time+10
                if password != '':  # если нет пароля, значит нет пользователя с введенным логином, поэтому записывать в историю входа не надо
                    time_entry = time.strftime("%d:%m:%Y %H:%M:%S", t)    # время неуспешной попытки входа
                    self.parent().facade.insert_time_entry(auth_log, time_entry, False)

                if self.count_try_entry == 2:
                    self.visible_captcha(True)
                    self.captcha_generation()
                    logging.log(logging.INFO, 'Ошибка. Вторая неуспешная попытка входа. Теперь введите капчу.')
                    self.mes_box('Вторая неуспешная попытка входа. Теперь введите капчу.')
                else:
                    logging.log(logging.INFO, 'Ошибка. Неправильно введены данные.')
                    self.mes_box('Неправильно введены данные.')
            elif password == auth_pas:
                time_entry = time.strftime("%d:%m:%Y %H:%M:%S", t)    # время успешной попытки входа
                self.parent().facade.insert_time_entry(auth_log, time_entry, True)
                logging.log(logging.INFO, 'Вход выполнен')
                self.parent().ui.lbl_fio.setText(fio)
                self.parent().ui.lbl_role.setText(role)
                if role == 'Старший смены' or role == 'Продавец':
                    self.parent().hide()
                    self.parent().page_id = [0, 2]
                    """Передать индексы страничек"""
                else:   # администратор
                    self.parent().hide()
                    self.parent().page_id = [0, 1, 4, 5]
                self.parent().show()
                self.parent().ui.lbl_photo.setPixmap(pix)
                self.parent().timer.start(1000)
                self.parent().now_login = auth_log
                self.close()


class DialogNewClient(QDialog):
    def __init__(self, parent=None):
        """
        Отвечает за подключением к кнопке "Добавить"
        """
        super(DialogNewClient, self).__init__(parent)
        self.ui = uic.loadUi("new_client.ui", self)
        self.facade = Facade()

        self.ui.btn_add_client.clicked.connect(self.add)

    def add(self):
        """
        Отвечает за добавление клиента в базу данных
        :return:
        """
        self.email = self.ui.edit_email.text()
        self.fio = self.ui.edit_fio.text()
        self.address = self.ui.edit_address.text()
        self.dateOfBirth = self.ui.date_birth.dateTime().toString('dd.MM.yyyy')
        self.passportData = self.ui.edit_passport.text()

        if self.fio != '' and self.passportData != '' and self.dateOfBirth != '' and self.address != '' and self.email != '':
            self.facade.insert_client(self.fio, self.passportData, self.dateOfBirth, self.address, self.email)
        else:
            self.mes_box('Заполните все поля!')

    def mes_box(self, text):
        """
        Открывает messagebox с переданным текстом.
        Вызывается, если какое-либо поле не заполнено.
        :param text: текст для вывода в messagebox
        """
        self.messagebox = QMessageBox(self)
        self.messagebox.setWindowTitle("Ошибка")
        self.messagebox.setText(text)
        self.messagebox.setStandardButtons(QMessageBox.Ok)
        self.messagebox.show()


class Builder:
    """
    Паттерн строитель.
    Это порождающий паттерн проектирования, который позволяет создавать сложные объекты пошагово.
    """
    def __init__(self):
        self.qapp = QApplication(sys.argv)
        self.window = MainWindow()
        self.auth()

    def auth(self):
        self.window.open_auth()
        self.qapp.exec()


if __name__ == '__main__':
    B = Builder()
