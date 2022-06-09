from database import Database


class Facade:
    def __init__(self):
        self.db = Database()

    def get_for_authorization(self, login):
        """ вернуть из бд пароль, роль сотрудника, дату последнего выхода и блокировку (true, false) по логину, если такого логина нет, тогда вернуть '', '', '', '' (4 пустых строки) """
        password, role, last_exit, block = '1', 'Администратор', '09:06:2022 00:49:00', True  # временные данные
        return password, role, last_exit, block

    def insert_time_entry(self, login, time, success):
        """вставить данные time_error_entry, success - успешная или ошибочная попытка входа (true, false) в таблицу истории входа) """
        pass
