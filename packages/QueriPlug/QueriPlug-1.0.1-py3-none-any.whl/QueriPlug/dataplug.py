import sqlite3


class Connection:

    def __init__(self, name: str):
        """
        :param name: The name of the database.
        """
        self.name = name
        self._conn = sqlite3.connect(self.name + ".db")
        self._cr = self._conn.cursor()


class TableConnection(Connection):

    def __init__(self, db: str | Connection, tablename: str, structure: list[tuple[str, str]]):
        """
        :param db: Name of database or Connection to database.
        :param tablename: Name of table.
        :param structure: The properties of each element in the table.
        """
        if type(db) == str: super().__init__(db)
        self.cursor = self._cr if type(db) == str else db._cr
        self.tablename = tablename
        self.struct = structure
        self.setupTable(structure)

    def _query(self, query: str) -> list:
        self.cursor.execute(query)
        self.cursor.connection.commit()
        return self.cursor.fetchall()

    def setupTable(self, structure: list[tuple[str, str]]) -> None:
        query = f"""CREATE TABLE IF NOT EXISTS {self.tablename} (ID INTEGER PRIMARY KEY,
            {''.join([structure[i][0] + " " + structure[i][1] + ", " for i in range(len(structure))])}"""[:-2] + ")"
        self._query(query)

    def getTable(self, *headings: str) -> list:
        query = """SELECT %s FROM %s;""" % (','.join(headings), self.tablename)
        out = self._query(query)
        for ind, item in enumerate(out):
            out[ind] = (item[0], *[item[i].replace(',', '') for i in range(1, len(item))])
        return out

    def clear(self) -> None:
        query = """DELETE FROM %s;""" % self.tablename
        self._query(query)

    def deleteElement(self, *elements) -> None:
        query = """DELETE FROM %s WHERE (ID) IN (%s);""" % (self.tablename, ','.join(str(elements)))
        self._query(query)

    def addElement(self, *values) -> None:
        query = """INSERT INTO %s (%s) VALUES ('%s')""" % (
            self.tablename, "va", ','.join(str(values)))
        self._query(query)
