from database import Database


class Facade:
    def __init__(self):
        self.db = Database()

    def get_log(self, login):
        return self.db.get_log(login)
