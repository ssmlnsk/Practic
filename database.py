import mysql
from mysql.connector import connect, Error


class Database:
    """
    Класс с функциями для взаимодействия с базой данных
    """
    def __init__(self):
        """
        Подключение к базе данных MySQL
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)
        finally:
            cursor.close()

    def insert_service(self, name, code, cost):
        """
        Добавление новой услуги
        :param name: наименование услуги
        :param code: код услуги
        :param cost: стоимость руб. за час
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO services VALUES (NULL, %s, %s, %s)", (name, code, cost))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_request(self, number, date, time, client, service):
        """
        Добавление нового заказа
        :param number: номер заказа
        :param date: дата создания
        :param time: время создания
        :param client: номер клиента
        :param service: услуги
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO requests VALUES (NULL, %s, %s, %s, %s, %s, NULL, NULL, NULL)", (number, date, time, client, service))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def update_service(self, id, name, code, cost):
        """
        Обновление услуг
        :param id: id услуги
        :param name: наименование услуги
        :param code: код услуги
        :param cost: стоимость руб. за час
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"UPDATE services set `Наименование услуги`='{name}', `Код услуги`='{code}', `Стоимость  руб.  за час`='{cost}' WHERE ID='{id}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def delete_service(self, id):
        """
        Удаление услуги
        :param id: id услуги
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM services WHERE ID='{id}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_clients(self):
        """
        Получение списка клиентов
        :return: rows
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM clients")
            rows = cursor.fetchall()

            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_employees(self):
        """
        Получение списка сотрудников
        :return: rows
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM employees")
            rows = cursor.fetchall()

            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_services(self):
        """
        Получение списка услуг
        :return: rows
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM services")
            rows = cursor.fetchall()

            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_info(self, login):
        """
        Получение информации о сотруднике
        :param login: логин сотрудника
        :return: log
        """
        log = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"""SELECT Пароль, Должность, `Последний вход`, `Тип входа`, ФИО, Фото FROM employees WHERE Логин = '{login}'""")
            rows = cursor.fetchall()

            for i in rows:
                for j in i:
                    log.append(j)
            return log

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_logins(self):
        """
        Получение списка логинов сотрудников
        :return: logins
        """
        logins = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"""SELECT Логин FROM employees""")
            rows = cursor.fetchall()

            for i in rows:
                for j in i:
                    logins.append(j)
            return logins

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_code_client(self, fio):
        """
        Получение кода и адреса клиента
        :param fio: ФИО клиента
        :return: client
        """
        client = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"""SELECT `Код клиента`, Адрес FROM clients WHERE ФИО='{fio}'""")
            rows = cursor.fetchall()
            for i in rows:
                for j in i:
                    client.append(j)
            return client

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_clients(self):
        """
        Получение списка ФИО клиентов
        :return: clients
        """
        clients = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT ФИО FROM clients")
            rows = cursor.fetchall()

            for i in rows:
                clients.append(str(i)[2:-3])
            return clients

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_client(self, fio, passportData, dateOfBirth, address, email):
        """
        Добавление нового клиента
        :param fio: ФИО
        :param passportData: Паспортные данные
        :param dateOfBirth: Дата рождения
        :param address: Адрес
        :param email: E-mail
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clients VALUES (%s, NULL, %s, %s, %s, %s, NULL)", (fio, passportData, dateOfBirth, address, email))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_services(self):
        """
        Получение списка наименований услуг
        :return: services
        """
        services = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT `Наименование услуги` FROM services")
            rows = cursor.fetchall()

            for i in rows:
                services.append(str(i)[2:-3])
            return services

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_serv_id(self, name):
        """
        Получение кода услуги
        :param name: Наименование услуги
        :return: row
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT ID FROM services WHERE `Наименование услуги`='{name}'")
            row = str(cursor.fetchone())
            return row[1:-2]

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_client_id(self, fio):
        """
        Получение кода клиента
        :param fio: ФИО
        :return: row
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT `Код клиента` FROM clients WHERE ФИО='{fio}'")
            row = str(cursor.fetchone())
            return row[1:-2]

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_time_entry(self, login, time, success):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param success: успешная или ошибочная попытка входа
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO history VALUES (NULL, %s, NULL, %s, %s)", (time, success, login))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_time_exit(self, login, time, block):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param block: нужен ли блок
        :return: None
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO history VALUES (NULL, NULL, %s, %s, %s)", (time, block, login))
            self.conn.commit()
            cursor.execute(f"UPDATE employees set `Последний вход`='{time}', `Тип входа`='{block}' WHERE `Логин`='{login}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_history(self):
        """
        Получение истории входа сотрудников
        :return:
        """
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM history")
            rows = cursor.fetchall()

            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()
