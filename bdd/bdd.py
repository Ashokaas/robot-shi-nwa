import sqlite3 as sql


class BDD:
    def __init__(self, file_name: str):
        self.file = sql.connect(file_name)
        self.cursor = self.file.cursor()
        self.requests = {"0":
                             "INSERT INTO robot (Exploration, Distance, Date, NSIum, Pilote)"
                             "VALUES (?, ?, date('now'), ?, ?);",
                         "1":
                             "SELECT * FROM robot"
                             "WHERE Pilote=? AND Exploration=?"}

    def request(self, request_id, list_args: tuple or list):
        request = self.requests[str(request_id)]
        results = self.cursor.execute(request, list_args)

        self.file.commit()
        return results

    def close(self):
        self.file.close()
