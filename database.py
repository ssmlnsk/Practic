import mysql
from mysql.connector import connect, Error


class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)
        finally:
            cursor.close()

    def insert_service(self, name, code, cost):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO services VALUES (NULL, %s, %s, %s)", (name, code, cost))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_request(self, number, date, time, client, service):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO requests VALUES (NULL, %s, %s, %s, %s, %s, NULL, NULL, NULL)", (number, date, time, client, service))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def update_service(self, id, name, code, cost):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"UPDATE services set `Наименование услуги`='{name}', `Код услуги`='{code}', `Стоимость  руб.  за час`='{cost}' WHERE ID='{id}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def delete_service(self, id):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"DELETE FROM services WHERE ID='{id}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_clients(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        log = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        logins = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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

    def get_clients(self):
        clients = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO clients VALUES (%s, NULL, %s, %s, %s, %s, NULL)", (fio, passportData, dateOfBirth, address, email))
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_services(self):
        services = []
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1',
                                                database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT ID FROM services WHERE `Наименование услуги`='{name}'")
            rows = str(cursor.fetchone())
            return rows[1:-2]

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_client_id(self, fio):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT `Код клиента` FROM clients WHERE ФИО='{fio}'")
            rows = str(cursor.fetchone())
            return rows[1:-2]

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_time_entry(self, login, time, success):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"INSERT INTO history VALUES (NULL, %s, NULL, %s, %s)", (time, success, login))
            self.conn.commit()
            cursor.execute(
                f"UPDATE employees set `Последний вход`='{time}', `Тип входа`='{success}' WHERE `Логин`='{login}'")
            self.conn.commit()

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def insert_time_exit(self, login, time, block):
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
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
        try:
            self.conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='iejahjoU1', database='igora')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM history")
            rows = cursor.fetchall()

            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()


if __name__ == '__main__':
    db = Database()
    # db.insert_service("test", "FN5SE4NIU6", 9600)
    # db.delete_service(355)
    # db.get_clients()
    # db.get_serv_id("Прокат шлема")
    # db.get_client_id("Фролов Андрей Иванович")
