from sqlite3 import connect


class Connection:
    """
    A connection to a databse, that can be used as the pointed database for all derived Connections
    """

    def __init__(self, name: str):
        """
        :param name: The name of the database.
        """
        self.name = name
        self._conn = connect(self.name + ".db")
        self._cr = self._conn.cursor()

    def _query(self, query: str) -> list:
        """
        :param query: The query to be sent to the database.
        :return: The result of the query.
        """
        self._cr.execute(query)
        self._cr.connection.commit()
        return self._cr.fetchall()


class TableConnection(Connection):
    """
    A type of Connection, that points to and edits tables.
    """

    def __init__(self, db: str | Connection, tablename: str, structure: list[tuple[str, str]]):
        """
        :param db: Name of database or Connection to database.
        :param tablename: Name of table.
        :param structure: The properties of each element in the table.
        """
        if type(db) == str:
            super().__init__(db)
        else:
            self._query = db._query

        self.cursor = self._cr if type(db) == str else db._cr
        self.tablename = tablename
        self.struct = structure
        self.setupTable(structure)

    def setupTable(self, structure: list[tuple[str, str]]) -> None:
        query = f"""CREATE TABLE IF NOT EXISTS {self.tablename} (ID INTEGER PRIMARY KEY,
            {''.join([structure[i][0] + " " + structure[i][1] + ", " for i in range(len(structure))])}"""[:-2] + ")"
        self._query(query)

    def getTable(self, *headings: str) -> list:
        """
        :param headings: The columns to read from.
        :return: The columns read from.
        """
        query = """SELECT %s FROM %s;""" % (','.join(headings), self.tablename)
        return self._query(query)

    def clear(self) -> None:
        """
        Clears the entire table.
        :return:
        """
        query = """DELETE FROM %s;""" % self.tablename
        self._query(query)

    def deleteElement(self, *elements) -> None:
        """
        Deletes the entries with the specified IDs.
        :param elements: The ID values to be deleted.
        :return:
        """
        query = """DELETE FROM %s WHERE (ID) IN (%s);""" % (self.tablename, ','.join(str(elements)))
        self._query(query)

    def addElement(self, *values) -> bool:
        if values in [i[1:] for i in self.getTable()]:
            return False
        query = """INSERT INTO %s (%s) VALUES %s""" % (
            self.tablename, ','.join([col[0] for col in self.struct]), ''.join(str(values)))
        self._query(query)
        return True
