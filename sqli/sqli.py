#  Barrowcroft, 2024

#  A simple interface for SQLite3.

import os
import os.path
import pprint
import sqlite3
from typing import Any


class SQLI:

    def __init__(self) -> None:
        """__init__

        Initialises the SQLite3 interface.

        """
        self._database: str = ""
        self._connection: sqlite3.Connection
        self._cursor: sqlite3.Cursor

    #  Fuctions to check database files.

    def database_open(self) -> bool:
        """database_open

        Checks that a database is open.
        A simple check that the database name has a value other than
        an empty string.

        Returns:
            bool: True, if a database is open.
        """
        if self._database == "":
            print("Error - there is no database open.")
            return False
        else:
            return True

    def database_valid(self, filename: str) -> bool:
        """database_valid

        Checks that a file is a valid database.

        Args:
            filename (str): The name of the file to check.

        Returns:
            bool: True, if the file is a valid database.
        """
        #  An empty file is valid.

        if os.path.getsize(filename) == 0:
            return True

        #  Check for valid database format.

        if os.path.getsize(filename) < 100:
            return False

        with open(filename, "rb") as fd:
            header = fd.read(100)
            if header[:16] != b"SQLite format 3\x00":
                return False

            return True

    #  Functions to manipulate database files.

    def create(self, database: str) -> bool:
        """create

        Creates an sqlite database.

        Args:
            database (str): name of database to create.

        Returns:
            bool: true, if successfully created.
        """
        if os.path.exists(database):
            print(f"Error - database '{database}' already exists.")
            return False

        try:
            self._database = database
            self._connection = sqlite3.connect(self._database)
            self._cursor = self._connection.cursor()

            print(f"Created database '{database}'.")
            return True
        except (sqlite3.DatabaseError, sqlite3.OperationalError, PermissionError) as e:
            print(f"Error - Could not create database '{database}' - {e}")
            self._connection.close()
            return False

    def open(self, database: str) -> bool:
        """open

        Opens an sqlite database.

        Args:
            database (str): name of database to open.

        Returns:
            bool: true, if successfully opened.
        """
        if not os.path.exists(database):
            print(f"Error - database '{database}' does not exist.")
            return False

        if not self.database_valid(database):
            print(f"Error - file '{database}' is not a valid database.")
            return False

        try:
            self._database = database
            self._connection = sqlite3.connect(self._database)
            self._cursor = self._connection.cursor()

            print(f"Opened database '{database}'.")
            return True
        except (sqlite3.DatabaseError, sqlite3.OperationalError, PermissionError) as e:
            print(f"Error - Could not open database '{database}' - {e}.")
            self._connection.close()
            return False

    def close(self) -> bool:
        """close

        Closes an sqlite database.

        Args:
            database (str): name of database to close.

        Returns:
            bool: true, if successfully close.
        """
        if self.database_open():
            print(f"Closing database '{self._database}'.")

            self._cursor.close()
            self._connection.close()

            self._database = ""

            return True
        else:
            return False

    #  Functions that execute sql statements.

    def execute_script(self, sql: str) -> None:
        """execute_script

        Executes an sql script. There wll be no results to return.

        Args:
            sql (str): sql script to execute.
        """
        _results: list[Any] = []

        if self.database_open():

            try:
                self._cursor = self._connection.executescript(sql)
                self._connection.commit()

            except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
                print(f"SQL Error - could not complete sql script - {e}.")

    def execute_sql(self, sql: str) -> list[Any]:
        """execute_sql

        Executes a single sql statement and returns the results.

        Args:
            sql (str): sql statement to execute.

        Returns:
            list[Any]: results of query.
        """
        _results: list[Any] = []

        if self.database_open():

            try:
                self._cursor = self._connection.execute(sql)
                self._connection.commit()
                _results = self._cursor.fetchall()

            except (sqlite3.DatabaseError, sqlite3.OperationalError) as e:
                print(f"SQL Error - could not complete sql statement - {e}.")

        return _results

    def execute(self, sql: str) -> None:
        """execute_sql

        Executes a single sql statement and prints the results.

        Args:
            sql (str): sql statement to execute.
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(sql)
            if _results == []:
                print("Query returned no results.")
            else:
                for _result in _results:
                    print(_result)

    def script(self, parms: dict[str, str]) -> None:
        """script

        Executes an sql script from a file. No results will be returned.

        Args:
            parms (dict[str, str]): paramters
                First parameter is the name of the script to open.
                Other parameters passed as needed by script.
        """
        if self.database_open():

            if len(parms) == 0:
                print("Error - expected name of script.")
                return
            
            _filename: str = parms["0"]

            #  Get the list of provided parameters.

            _parms:list[str] = []
            for _, _p in parms.items():
                _parms.append(_p)
            _parms = _parms[1:]

            try:
                with open(_filename, "r") as file:

                    _sql = file.read().replace("\n", " ")

                    #  Check number of expected parameters.

                    _expected:int = _sql.count("?") 
                    if _expected != len(_parms):
                        print(f"Error - incorrect number of parameters - {_expected} expected, {len(_parms)} supplied")
                        return
                    
                    #  Replace parameter markers (?) with parameters.

                    for i in range(len(_parms)):
                        _sql = _sql.replace("?",_parms[i],1)
                    print(_sql)

                    #  Execute modified script.

                    self.execute_script(_sql)
            except:
                print(f"Error - could not open script '{_filename}'.")


    def tables(self, _: dict[str, str]) -> None:
        """tables

        Prints a list of tables in the database.

        Args:
            _ (dict[str, str]): ignored!
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(
                "SELECT name FROM sqlite_master WHERE type='table';"
            )
            if _results == []:
                print("No tables in database.")
            else:
                for _result in _results:
                    print(_result[0])

    def indices(self, _: dict[str, str]) -> None:
        """indices

        Prints a list of indices in the database.

        Args:
            _ (dict[str, str]): ignored!
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(
                "SELECT name FROM sqlite_master WHERE type='index';"
            )
            if _results == []:
                print("No indices in database.")
            else:
                for _result in _results:
                    print(_result[0])

    def views(self, _: dict[str, str]) -> None:
        """views

        Prints a list of views in the database.

        Args:
            _ (dict[str, str]): ignored!
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(
                "SELECT name FROM sqlite_master WHERE type='view';"
            )
            if _results == []:
                print("No views in database.")
            else:
                for _result in _results:
                    print(_result[0])

    def triggers(self, _: dict[str, str]) -> None:
        """triggers

        Prints a list of triggers in the database.

        Args:
            _ (dict[str, str]): ignored!
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(
                "SELECT name FROM sqlite_master WHERE type='trigger';"
            )
            if _results == []:
                print("No triggers in database.")
            else:
                for _result in _results:
                    print(_result[0])

    def schema(self, _: dict[str, str]) -> None:
        """schema

        Prints the netire schema of the database.

        Args:
            _ (dict[str, str]): ignored!
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql("SELECT * FROM sqlite_master;")
            if _results == []:
                print("Database is empty.")
            else:
                pprint.pprint(_results)

    def describe(self, parms: dict[str, str]) -> None:
        """describe

        Prints a description (sql) of the given item.

        Args:
            parms (dict[str, str]): parameters
                "name" = name of item to describe.
        """
        if self.database_open():
            _results: list[Any] = self.execute_sql(
                f"SELECT * FROM sqlite_master WHERE name='{parms["name"]}';"
            )
            if _results != []:
                for _result in _results:
                    pprint.pprint(_result)
            else:
                print(f"There is no item by the name '{parms["name"]}'.")
