import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='admin',
            database='database',
        )

    def getCLients(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM CLIENTS")
        clients = cursor.fetchall()
        for i in clients:
            print(i)
        return clients

    def getRequests(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM REQUESTS")
        requests = cursor.fetchall()
        for i in requests:
            print(i)
        return requests

    def getEmployeers(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM EMPLOYEERS")
        employeers = cursor.fetchall()
        for i in employeers:
            print(i)
        return employeers

    def getServices(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM SERVICES")
        services = cursor.fetchall()
        for i in services:
            print(i)
        return services

    def getHistory(self):
        cursor = self.connection.cursor()
        cursor.exectue("SELECT * FROM EntryHistory")
        history = cursor.fetchall()
        for i in history:
            print(i)
        return history

    def insertСlients(self, name, number_client, passport, datebirth, address, email, password):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO clients "
            f"(`name`,`number_client`,`passport`,`datebirth`,`address`,`email`,`password`) "
            f"VALUES ('{name}','{number_client}', '{passport}', '{datebirth}', '{address}', '{email}', '{password}')")
        cursor.close()
        self.connection.commit()

    def insertEmployeers(self, id_employeer, post, name, login, password, lastLogIn, StatusLogIn):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO employeers"
            f"(`id_employeer`, `post`, `name`, `login`, `password`, `lastLogIn`, `StatusLogIn`) "
            f"VALUES ('{id_employeer}', '{post}', '{name}', '{login}', '{password}', '{lastLogIn}', '{StatusLogIn}' )")
        cursor.close()
        self.connection.commit()

    def insertServices(self, id_service, name_service, code_service, price_for_hour):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO services"
            f"(`id_service`, `name_service`, `code_service`, `price_for_hour`)"
            f"VALUES ('{id_service}', '{name_service}', '{code_service}', '{price_for_hour}')" )
        cursor.close()
        self.connection.commit()

    def insertRequests(self, id_request, number_request, date_create, time_request, number_client, services, status_request, rental_time):
        cursor = self.connection.cursor()
        cursor.execute(
            f"INSERT INTO requests"
            f"(`id_request`, `number_request`, `date_create`, `time_request`, `number_client`, `services`, `status_request`, `rental_time`)"
            f"VALUES ('{id_request}', '{number_request}', '{date_create}', '{time_request}', '{number_client}', '{services}', '{status_request}', '{rental_time}')"
        )
        cursor.close()
        self.connection.commit()


    def DeleteClients(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE clients")
        cursor.close()
        self.connection.commit()

    def DeleteRequests(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE requests")
        cursor.close()
        self.connection.commit()

    def DeleteServices(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE services")
        cursor.close()
        self.connection.commit()

    def DeleteEmployeers(self):
        cursor = self.connection.cursor()
        cursor.execute("DROP TABLE employeers")
        cursor.close()
        self.connection.commit()

if __name__ == '__main__':
    D = Database()
    print("All clients")
    print("___________________________________________________________________________________________________________")
    D.getCLients()
    print("---------------------------------------------------------------------------------")
    #print("All requests")
    #print("___________________________________________________________________________________________________________")
    #D.getRequests()
    #print("---------------------------------------------------------------------------------")
    #print("All employeers")
    #print("___________________________________________________________________________________________________________")
    #D.getEmployeers()
    #print("---------------------------------------------------------------------------------")
    #print("All services")
    #print("___________________________________________________________________________________________________________")
    #D.getServices()
    #D.insertСlients("Минаков Павел Сергеевич", 45462599, "Серия 7312 Номер 699088", "2003-09-05", "141410, г.Химки, ул. Маяковского, д.24, кв.23", "promtman1990@gmail.com", "abobasus")
    #D.getCLients()
    #D.insertEmployeers("ID 111", "Продавец", "Алексеев Иван Сергеевич", "example@yahoo.com", "qazwsxedc", "09.06.2022 14:00", "Успешно")
    #D.getEmployeers()
    D.insertServices("")
