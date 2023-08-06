'''
Contains the `Table` class used to represent tables in a
SQlite database.
'''

import sqlite3

class Table:
    '''
    Bundles SQlite tables and the available
    queries that can be performed on them into convenient
    helper methods.
    '''
    def __init__(self, table_name: str, columns=tuple[str]) -> None:
        self.table = table_name
        self.columns = columns
    def setCursor(self, cursor: sqlite3.Cursor) -> None:
        self.cursor = cursor
    def setConnection(self, connection: sqlite3.Connection) -> None:
        self.connection = connection
    def getColumns(self) -> tuple[str]:
        return self.columns
    def construct_named_parameters(self, data: list[tuple]) -> tuple:
        '''
        Python's `sqlite3` module requires named parameters to be
        passed to the `__parameters` parameter of the `sqlite3.Cursor.execute`
        method as a sequence containing dictionaries with keys corresponding
        to the named parameters specified in the SQL query as such:
        ```
        data = (
            {"name": "C", "year": 1972},
            {"name": "Fortran", "year": 1957},
            {"name": "Python", "year": 1991},
            {"name": "Go", "year": 2009},
        )
        cur.executemany("INSERT INTO lang VALUES(:name, :year)", data)
        ```
    
        In the above example the values at keys `"name"` and `"year"` for each
        dictionary are supplied as separate tuples to perform a multi-row insertion
        operation using the `sqlite3.Cursor.executemany` method. Such an operation, 
        beneath the abstraction, would be identical in syntax and effect to the following
        example:
        ``` 
        cur.execute("""
            INSERT INTO lang VALUES
                ("C", 1972),
                ("Fortran", 1957),
                ("Python", 1991),
                ("Go", 2009)
        """)
        ```

        Thus, in order to generate an iterable object containing column names
        within an SQL table, this method constructs a sequence of dictionaries 
        with key and value pairs that correspond to these specified column names
        as well as a string containing the keys formatted so that they can be 
        easily accessed using the `__parameters` parameter of the 
        `sqlite3.Cursor.executemany` method.

        This function returns a tuple containign two elements. The first element is
        the dictionary-containing sequence while the second element is the formatted
        string.

        :param data: A sequence containing tuples of data to be referenced
        durign a SQL query.
        '''
        # Initialize sequence for storing dictionaries
        named_parameters = tuple()
        # Initialize formatted string for representing each dictionary key
        parameter_string = str()

        for row in data:
            # Initialize dictionary to store this tuple's data
            data_dict = dict()
            for i in range(len(row)):
                # Concatenate key to formatted string
                if i != len(row) - 1:
                    parameter_string += f':{i}, '
                else:
                    # Exclude unnecessary trailing comma and space
                    # if current index represents the final parameter
                    parameter_string += f':{i}'

                # Create key-value pair with the key as an index
                # and the value being the element at the corresponding
                # index in the current tuple
                data_dict[i] = row[i]
            named_parameters += (data_dict,)
        return (named_parameters, parameter_string)
    
    def insertRows(self, row_data: list[tuple]) -> None:
        '''
        Inserts multiple rows of data into the Table.
        '''
        formatted_rows = self.construct_named_parameters(row_data)
        
        self.cursor.executemany(f"INSERT INTO {self.table} VALUES({formatted_rows[1]})", formatted_rows[0])
        self.connection.commit()
    def selectColumnData(self, column_names: tuple[str]) -> list[tuple]:
         '''
         Returns a list containing each row's value for the specified
         column(s). Row data is returned as a `tuple`.
         '''
         formatted_columns = self.construct_named_parameters(column_names)
         return self.cursor.execute(f"SELECT {formatted_columns[1]} FROM {self.table}", formatted_columns[0]).fetchall()
    