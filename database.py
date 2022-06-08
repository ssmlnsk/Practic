import mysql
from mysql.connector import connect, Error
from configparser import ConfigParser


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

    def select(self):
        try:
            self.conn = mysql.connector.connect(host='localhost', database='igora', user='root', password='iejahjoU1')
            cursor = self.conn.cursor()
            cursor.execute(f"SELECT * FROM clients")
            rows = cursor.fetchall()

            print('Total Row(s):', cursor.rowcount)
            for row in rows:
                print(row)

        except Error as e:
            print(e)

        finally:
            self.conn.close()
            cursor.close()


if __name__ == '__main__':
    db = Database()
    db.select()
