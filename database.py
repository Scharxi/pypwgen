import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.commit()
            self.conn.close()

    def execute(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        if params is None:
            params = ()
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
