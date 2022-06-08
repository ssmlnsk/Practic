import mysql
from mysql.connector import connect, Error


class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', database='igora', user='root', password='iejahjoU1')
            cursor = self.conn.cursor()
            if self.conn.is_connected():
                print('Connected to MySQL database')
        except Error as e:
            print(e)
        finally:
            self.conn.close()
            cursor.close()

    def select_clients(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', database='igora', user='root', password='iejahjoU1')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM clients")
            rows = cursor.fetchall()

            print('Total Row(s):', cursor.rowcount)
            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def select_employees(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', database='igora', user='root', password='iejahjoU1')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM employees")
            rows = cursor.fetchall()

            print('Total Row(s):', cursor.rowcount)
            return rows

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

    def get_log(self, login):
        log = []
        try:
            self.conn = mysql.connector.connect(host='localhost', database='igora', user='root', password='iejahjoU1')
            cursor = self.conn.cursor()
            cursor.execute(f"""SELECT Пароль, Должность, `Последний вход` FROM employees WHERE Логин = '{login}'""")
            rows = cursor.fetchall()

            print('Total Row(s):', cursor.rowcount)
            for i in rows:
                for j in i:
                    log.append(j)
            return log

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()

