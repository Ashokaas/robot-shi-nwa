import sqlite3 as sql


class BDD:
    def __init__(self, file_name: str):
        self.file = sql.connect(file_name, check_same_thread=False)
        self.cursor = self.file.cursor()
        self.requests = {"add":
                             "INSERT INTO robot (Exploration, Distance, Date, NSIum, Pilote)"
                             "VALUES (?, ?, date('now'), ?, ?);",
                         "get":
                             "SELECT DISTINCT Exploration, Date, Pilote FROM robot "
                             "WHERE Pilote LIKE ? AND Exploration LIKE ? AND Date LIKE ?;",
                         "get_datas":
                             "SELECT * FROM robot "
                             "WHERE Pilote = ? AND Exploration = ? AND Date = ?;",
                         "get_all_exploration":
                             "SELECT DISTINCT Exploration FROM robot;",
                         "get_all_pilote":
                             "SELECT DISTINCT Pilote FROM robot;",
                         }

    def request(self, request_id, list_args: list) -> list:
        if request_id == "get":
            for i in range(len(list_args)):
                list_args[i] += "%"

        request = self.requests[str(request_id)]
        results = self.cursor.execute(request, list_args)

        self.file.commit()
        return results.fetchall()

    def close(self):
        self.file.close()
