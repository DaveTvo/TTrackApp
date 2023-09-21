import sqlite3
from typing import List


class DatabaseHandler:

    def __init__(self, db_name='my_database.db', **kwargs):
        super(DatabaseHandler, self).__init__(**kwargs)
        self._db_name = db_name
        self._db_connection = self.get_database_connection()
        self._cursor = self._db_connection.cursor()

    def get_database_connection(self):
        return sqlite3.connect(self._db_name)

    def close_db_connection(self):
        self._db_connection.close()

    def select_from_table(self, table_name):
        # Protect against SQL injection for table names
        if table_name in ['trainings', 'exercises']:
            self._cursor.execute(f"SELECT * FROM {table_name}")
            rows = self._cursor.fetchall()
            for row in rows:
                print(row)

    def commit(self):
        self._db_connection.commit()

    @property
    def db_connection(self):
        return self._db_connection


class TrainingsTable(DatabaseHandler):

    def __init__(self, **kwargs):
        super(TrainingsTable, self).__init__(**kwargs)

    @staticmethod
    def create_trainings_table(connection) -> None:
        connection.execute('''
        CREATE TABLE IF NOT EXISTS trainings (
            training_id INTEGER PRIMARY KEY,
            training_name TEXT NOT NULL,
            training_time INTEGER
        )
        ''')

    def add_training(self, training_name: str, training_time: int) -> None:
        self._cursor.execute("INSERT INTO trainings (training_name, training_time) VALUES (?, ?)",
                             (training_name, training_time))
        self.commit()

    def update_training_name(self, training_name, training_id):
        self._cursor.execute("UPDATE trainings SET training_name = ? WHERE training_id = ?",
                             (training_name, training_id))
        self.commit()

    def update_training_time(self, training_time, training_id):
        self._cursor.execute("UPDATE trainings SET training_time = ? WHERE training_id = ?",
                             (training_time, training_id))
        self.commit()

    def delete_training(self, training_id):
        self._cursor.execute("DELETE FROM trainings WHERE training_id = ?", (training_id,))
        self.commit()


class ExerciseTable(DatabaseHandler):

    def __init__(self, **kwargs):
        super(ExerciseTable, self).__init__(**kwargs)

    @staticmethod
    def create_exercise_table(connection) -> None:
        connection.execute('''
        CREATE TABLE IF NOT EXISTS exercises (
            exercise_id INTEGER PRIMARY KEY,
            training_id INTEGER,
            exercise_unit TEXT,
            exercise_series_amount INTEGER,
            exercise_values TEXT
        )
        ''')

    def add_exercise(self, training_id: int, exercise_unit: str, exercise_series_amount: int, values: List[int]):
        if exercise_unit in ['Weight', 'Time', 'Distance']:
            values_str = ",".join(map(str, values))
            self._cursor.execute(
                "INSERT INTO exercises (training_id, exercise_unit, exercise_series_amount, exercise_values) VALUES (?, ?, ?, ?)",
                (training_id, exercise_unit, exercise_series_amount, values_str))
            self.commit()
