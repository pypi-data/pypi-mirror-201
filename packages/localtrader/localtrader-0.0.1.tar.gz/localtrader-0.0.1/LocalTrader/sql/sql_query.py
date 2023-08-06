
import sqlite3
from .sql_table import Table

class Query:
    '''
    Base class for executing SQL queries on a 
    database.
    '''
    def __init__(self, filename: str) -> None:
        self.db_filename = filename
        self.cursor = None
    def connect(self, timeout: float) -> sqlite3.Connection:
        self.connection = sqlite3.connect(database=self.db_filename, timeout=timeout)
        return self.connection
    def createCursor(self) -> sqlite3.Cursor:
        '''
        Attempts to retrieve and return a cursor for this
        instance's sqlite3 database connection. If one does
        not exist, it initializes and returns a new one.
        '''
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor
    def createTable(self, table_name: str, columns=tuple[str]) -> None:
        '''
        Create and return a new instance of the `Table` class.
        '''
        self.cursor.execute(f"CREATE TABLE {table_name}{columns}")
        return Table(table_name, columns)
    def createRow(self, table_name: str, row_data: tuple) -> None:
        self.cursor.execute(f"""
            INSERT INTO {table_name} VALUES
                {row_data}
        """)
        self.connection.commit()
    def createColumn(self, table_name: str, column: str) -> None:
        self.cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column}")

class EquityQuery(Query):
    '''
    Provides access to executing SQL queries on 
    tables contaning data on a specific equity.
    '''
    def __init__(self, filename: str, equity: str) -> None:
        super().__init__(filename)
        self.equity = equity
    def addEquity(self) -> None:
        if not self.cursor:
            super().createCursor()
        super().createTable(self.equity.lower(), ("indicators"))

class PriceQuery(Query):
    '''
    Provides access to executing SQL queries on 
    tables containing price data for a specific
    equity.
    '''
    def __init__(self, filename: str, equity: str) -> None:
        super().__init__(filename)
        self.equity = equity


class AuthenticationQuery(Query):
    '''
    Provides access to executing SQL queries on
    tables containing OAuth token data.
    '''
    def __init__(self, filename: str) -> None:
        super().__init__(filename)