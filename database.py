import sqlite3


class Database:
    def __init__(self, db_file) -> None:
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def cbdt(self):
        with self.connection:
            create = """ CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER,
                    login TEXT,
                    password TEXT)"""
            self.cursor.execute(create)

    def user_exist(self, telegram_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchmany(1)
            return bool(len(result))

    def create_user(self, telegram_id, login, password):
        with self.connection:
            return self.cursor.execute(f"INSERT INTO users(telegram_id, login, password) VALUES(?, ?, ?)", (
                telegram_id, login, password))

    def get_udata(self, telegram_id):
        with self.connection:
            exist = " SELECT * FROM users WHERE telegram_id = ? "
            if [data for data in self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchmany(1)] == []:
                pass
            else:
                return [data for data in self.cursor.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)).fetchmany(1)][0][2:4]

    def all_users(self):
        with self.connection:
            exist = f"""SELECT * FROM users"""

            return [data for data in self.cursor.execute(exist)]

    def remove(self, telegram_id):
        with self.connection:
            self.cursor.execute(
                "DELETE FROM users WHERE telegram_id = ?", (telegram_id,))
