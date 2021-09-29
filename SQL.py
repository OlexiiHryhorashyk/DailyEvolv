import sqlite3


class SqlManage:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id, name, gender, age, height, weight, fat, sport, program, day, cycle):
        with self.connection:
            sql = '''INSERT INTO users('user_id', 'name', 'gender', 'age', 'height', 'weight', 'fat', 'sport', 
            'program', day, cycle) VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
            return self.cursor.execute(sql, (user_id, name, gender, age, height, weight, fat, sport, program, day, cycle,))

    def delete_user(self, user_id):
        with self.connection:
            return self.cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,)).fetchall()

    def get_user_by_id(self, user_id):
        with self.connection:
            user = {
                'name': self.cursor.execute("SELECT name FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'gender': self.cursor.execute("SELECT gender FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'age': self.cursor.execute("SELECT age FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'sport': self.cursor.execute("SELECT sport FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'program': self.cursor.execute("SELECT program FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'day': self.cursor.execute("SELECT day FROM users WHERE user_id = ?", (user_id,)).fetchone(),
                'cycle': self.cursor.execute("SELECT cycle FROM users WHERE user_id = ?", (user_id,)).fetchone(),
            }
            return user

    # def get_users_id(self):
    #     with self.connection:
    #         return self.cursor.execute("SELECT user_id FROM users").fetchall()

    def get_user_day(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT day FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result

    def get_user_cycle(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT cycle FROM users WHERE user_id = ?", (user_id,)).fetchone()
            return result

    def set_user_day(self, day, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET day = ? WHERE user_id = ?", (day, user_id,)).fetchone()

    def set_user_cycle(self, cycle, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET cycle = ? WHERE user_id = ?", (cycle, user_id,)).fetchone()
