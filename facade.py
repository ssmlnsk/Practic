from database import Database


class Facade:
    def __init__(self):
        self.db = Database()

    def get_logins(self):
        return self.db.get_logins()

    def get_for_authorization(self, login):
        log = self.db.get_info(login)
        """ вернуть из бд пароль, роль сотрудника, дату последнего выхода и блокировку (true, false) по логину, если такого логина нет, тогда вернуть '', '', '', '' (4 пустых строки) """
        password, role, last_exit, block, fio = log[0], log[1], log[2], True, log[3]  # временные данные
        return password, role, last_exit, block, fio

    def insert_time_entry(self, login, time, success):
        """вставить данные time_error_entry, success - успешная или ошибочная попытка входа (true, false) в таблицу истории входа) """
        pass

    def read_clients(self):
        return self.db.select_clients()

    def read_services(self):
        return self.db.select_services()

    def insert_time_entry(self, login, time, success):
        """вставить данные time, success - успешная или ошибочная попытка входа (true, false) в таблицу истории входа и заменить в таблице сотрудника (последний вход и успех) по логину) """
        pass

    def insert_time_exit(self, login, time, block):
        """вставить данные time - время выхода, block - нужен ли блок (true, false) в таблицу истории входа по логину) """
        pass