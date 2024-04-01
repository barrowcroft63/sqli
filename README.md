# sqli
# A simple SQLite interface

Installation: 

`Install using: pip install git+https://github.com/barrowcroft63/sqli.git`

### Use:

Create the SQLI object:

`sqli:SQLI = SQLI()`

The SQLIobject provides the folowing methods:

| Method                        | Purpose                          |
|-------------------------------|----------------------------------|
|sqli.database_open(filename)|Checks that a database is open.|
|sqli.database_valid(filename)|Checks that a file is a valid database|
|sqli.create(filename)|Creates an sqlite database.|
|sqli.open(filename)|Opens an sqlite database.|
|sqli.close()|Closes an sqlite database.|
|sqli.execute_script(script)|Executes an sql script. There wll be no results to return.|
|sqli.execute_sql(statement)|Executes a single sql statement and returns the results.|
|sqli.execute(statement)|Executes a single sql statement and prints the results.|
|sqli.script(parms)|Executes an sql script from a file. No results will be returned.*|
|sqli.tables()|Prints a list of tables in the database.|
|sqli.indices()|Prints a list of indices in the database.|
|sqli.views()|Prints a list of views in the database.|
|sqli.triggers()|Prints a list of triggers in the database.|
|sqli.schema()|Prints the netire schema of the database.|
|sqli.describe(item_name)|Prints a description (sql) of the given item.|

Parameters will be:
```
parms (dict[str, str]): paramters
    First parameter is the name of the script to open.
    Other parameters passed as needed by script.
```
