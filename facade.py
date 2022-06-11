from database import Database


class Facade:
    def __init__(self):
        self.db = Database()

    def get_logins(self):
        return self.db.get_logins()

    def get_clients(self):
        return self.db.get_clients()

    def get_services(self):
        return self.db.get_services()

    def get_id_serv(self, name):
        return self.db.get_serv_id(name)

    def get_id_client(self, fio):
        return self.db.get_client_id(fio)

    def get_for_authorization(self, login):
        log = self.db.get_info(login)
        """ вернуть из бд пароль, роль сотрудника, дату последнего выхода и блокировку (true, false) по логину, если такого логина нет, тогда вернуть '', '', '', '' (4 пустых строки) """
        password, role, last_exit, block, fio = log[0], log[1], log[2], True, log[3]  # временные данные
        return password, role, last_exit, block, fio

    def insert_service(self, name, code, cost):
        self.db.insert_service(name, code, cost)

    def delete_service(self, id):
        self.db.delete_service(id)

    def update_service(self, id, name, code, cost):
        self.db.update_service(id, name, code, cost)

    def create_request(self, number, date, time, client, service):
        self.db.insert_request(number, date, time, client, service)

    def read_clients(self):
        return self.db.select_clients()

    def read_history(self):
        return self.db.select_history()

    def insert_client(self, fio, passportData, dateOfBirth, address, email):
        self.db.insert_client(fio, passportData, dateOfBirth, address, email)

    def read_services(self):
        return self.db.select_services()

    def insert_time_entry(self, login, time, success):
        """вставить данные time, success - успешная или ошибочная попытка входа (true, false) в таблицу истории входа и заменить в таблице сотрудника (последний вход и успех) по логину) """
        self.db.insert_time_entry(login, time, success)

    def insert_time_exit(self, login, time, block):
        """вставить данные time - время выхода, block - нужен ли блок (true, false) в таблицу истории входа по логину) """
        self.db.insert_time_exit(login, time, block)
