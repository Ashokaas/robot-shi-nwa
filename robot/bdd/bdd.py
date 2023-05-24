import sqlite3 as sql


class BDD:
    def __init__(self, file_name: str):
        self.file = sql.connect(file_name)
        self.cursor = self.file.cursor()
        self.requests = {"0":
                             "INSERT INTO robot (Exploration, Distance, NSIum)"
                             "VALUES (?, ?, ?);"}

    def request(self, request_id, list_args: tuple or list):
        request = self.requests[request_id]
        results = self.cursor.execute(request, list_args)

        self.file.commit()

    def close(self):
        self.file.close()
