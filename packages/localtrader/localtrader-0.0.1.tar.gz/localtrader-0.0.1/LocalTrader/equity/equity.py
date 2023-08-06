'''
Contains the `Equity` class, an object used to
represent tradeable assets.
'''

import sqlite3
from sql import sql_table

class Equity:
    '''
    ```
    spy = Equity("SPY")
    
    ```
    '''
    def __init__(self, ticker: str, cursor: sqlite3.Cursor) -> None:
        self.ticker = ticker
        self.cursor = cursor
    def get_table(self) -> sql_table.Table | None:
        '''
        Returns an instance of the `Table` class if a table corresponding
        to the equity specified in `self.ticker` exists in the SQlite database.
        If one does not exist, it returns `None`.
        '''
        table = self.cursor.execute(f"SELECT {self.ticker} FROM sqlite_master").fetchone()
        if table is not None:
            return sql_table.Table(self.ticker)
    def create_or_get_table(self) -> sql_table.Table:
        '''
        Attempts to retrieve the table corresponding to the ticker
        associated with this instance of the `Equity` class. If one 
        does not exist, it creates one.
        '''
        if self.get_table() is None:
            self.cursor.execute(f"CREATE TABLE {self.ticker}")
        return sql_table.Table(self.ticker)