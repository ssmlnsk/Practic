from database import Database


class Facade:
    """
    Класс фасада
    """
    def __init__(self):
        """
        Создание объекта БД
        """
        self.db = Database()

    def get_logins(self):
        """
        Получение списка логинов сотрудников
        :return: список логинов
        """
        return self.db.get_logins()

    def get_code_client(self, fio):
        """
        Получение кода и адреса клиента
        :param fio: ФИО
        :return: код и адрес клиента
        """
        return self.db.get_code_client(fio)

    def get_clients(self):
        """
        Получение списка клиентов
        :return: Список клиентов
        """
        return self.db.get_clients()

    def get_services(self):
        """
        Получение списка услуг
        :return: Список услуг
        """
        return self.db.get_services()

    def get_id_serv(self, name):
        """
        Получение кода услуги
        :param name: Наименование услуги
        :return: код услуги
        """
        return self.db.get_serv_id(name)

    def get_id_client(self, fio):
        """
        Получение кода клиента
        :param fio:
        :return:
        """
        return self.db.get_client_id(fio)

    def get_for_authorization(self, login):
        """
        Получение информации о сотруднике
        :param login: Логин
        :return: password, role, last_exit, block, fio, photo
        """
        log = self.db.get_info(login)
        if log == []:
            return '', '', '', '', '', ''
        password, role, last_exit, block, fio, photo = log[0], log[1], log[2], log[3], log[4], log[5]  # временные данные
        return password, role, last_exit, block, fio, photo

    def insert_service(self, name, code, cost):
        """
        Добавление услуги
        :param name: Наименование услуги
        :param code: Код услуги
        :param cost: Стоимость руб. за час
        :return: None
        """
        self.db.insert_service(name, code, cost)

    def delete_service(self, id):
        """
        Удаление услуги
        :param id: id услуги
        :return: None
        """
        self.db.delete_service(id)

    def update_service(self, id, name, code, cost):
        """
        Обновление таблицы услуг
        :param id: id услуги
        :param name: Наименование услуги
        :param code: Код услуги
        :param cost: Стоимость руб. за час
        :return: None
        """
        self.db.update_service(id, name, code, cost)

    def create_request(self, number, date, time, client, service):
        """
        Создание заказа
        :param number: Номер заказа
        :param date: Дата создания
        :param time: Время создания
        :param client: Код клиента
        :param service: Код услуги
        :return: None
        """
        self.db.insert_request(number, date, time, client, service)

    def read_clients(self):
        """
        Получение списка клиентов
        :return: Список клиентов
        """
        return self.db.select_clients()

    def read_history(self):
        """
        Получение списка истории входа
        :return: список истории входа
        """
        return self.db.select_history()

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
        self.db.insert_client(fio, passportData, dateOfBirth, address, email)

    def read_services(self):
        """
        Получение списка услуг
        :return: Список услуг
        """
        return self.db.select_services()

    def insert_time_entry(self, login, time, success):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param success: успешная или ошибочная попытка входа
        :return: None
        """
        self.db.insert_time_entry(login, time, success)

    def insert_time_exit(self, login, time, block):
        """
        Добавление времени входа сотрудника
        :param login: Логин
        :param time: Дата и время
        :param block: нужен ли блок
        :return: None
        """
        self.db.insert_time_exit(login, time, block)

    def get_date_serv(self):
        return self.db.get_date_serv()
