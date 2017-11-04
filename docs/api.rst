API
===


**class dataswim.DataSwim(db=None)**

    Bases: dataswim.Db, dataswim.Df

    Main class

    **add** (``field``, ``value``)

        Add a columns with default values

    **concat** (``dfs``)

        Concatenate dataframes from a list and set it to the main dataframe

    **connect** (``url``)

        Connect to the database and set it as main database

    **contains** (``value``, ``field``)

        Returns rows that contains a string value in a column

    **count** ()

        Count the number of rows of the main dataframe

    **count_rows** (``name``, ``p=True``)

        Count rows for a table

    **date** (``fields``)

        Convert column values to datetime from either a list of column names or a single column name string

    **date_field** (``field``)

        Add a date column from the datetime index

    **describe** ()

        Print a description of the data in notebook

    **display** (``fields``)

        Display some columns head in notebook

    **drop** ()

        Drop NaN values from the main dataframe

    **exact** (``value``, ``field``)

        Returns rows that has the exact string value in a column

    **fill** (``fieldname``, ``val=0``)

        Fill NaN values with new values

    **getall** (``table``)

        Get all rows values for a table

    **head** ()

        Print the main dataframe’s head in notebook

    **index** (``datafield``, ``indexfield``)

        Set a datetime index from a column

    **load** (``table``)

        Set the main dataframe from a table’s data

    **look** (``df=None``, ``p=True``)

        Print basic data info in notebook

    **nulls** (``fieldname``, ``val=0``)

        Fill null values with new values

    **range** (``num``, ``unit``)

        Limit the data in a time range

    **reduce** (``fields``)

        Limit a dataframe to some columns

    **report** (``df=None``)

        Returns a dataframe profiling report to print in notebooks

    **resample** (``time_unit='1Min'``, ``date_field=None``)

        Resample the main dataframe to a time period

    **set** (``df``)

        Set a main dataframe

    **show** (``table=None``, ``p=True``)

        Display info about a table

    **tables** (``name=None``, ``p=True``)

        Print existing tables in a database

    **to_int** (``fieldname``)

        Convert a column values to integers
        

Database operations
-------------------

class dataswim.Db** (``db=None``)

    Bases: object

    Class for manipulating databases

    **connect** (``url``)

        Connect to the database and set it as main database

    **count_rows** (``name``, ``p=True``)

        Count rows for a table

    **getall** (``table``)

        Get all rows values for a table

    **load** (``table``)

        Set the main dataframe from a table’s data

    **show** (``table=None``, ``p=True``)

        Display info about a table

    **tables** (``name=None``, ``p=True``)

        Print existing tables in a database
        
Dataframe operations
--------------------

class **dataswim.Df** (``df=None``)

    Bases: object

    Class for manipulating dataframes

    **add** (``field``, ``value``)

        Add a columns with default values

    **concat** (``dfs``)

        Concatenate dataframes from a list and set it to the main dataframe

    **contains** (``value``, ``field``)

        Returns rows that contains a string value in a column

    **count** ()

        Count the number of rows of the main dataframe

    **date** (``fields``)

        Convert column values to datetime from either a list of column names or a single column name string

    **date_field** (``field``)

        Add a date column from the datetime index

    **describe** ()

        Print a description of the data in notebook

    **display** (``fields``)

        Display some columns head in notebook

    **drop** ()

        Drop NaN values from the main dataframe

    **exact** (``value``, ``field``)

        Returns rows that has the exact string value in a column

    **fill** (``fieldname``, ``val=0``)

        Fill NaN values with new values

    **head** ()

        Print the main dataframe’s head in notebook

    **index** (``datafield``, ``indexfield``)

        Set a datetime index from a column

    **look** (``df=None``, ``p=True``)

        Print basic data info in notebook

    **nulls** (``fieldname``, ``val=0``)

        Fill null values with new values

    **range** (``num``, ``unit``)

        Limit the data in a time range

    **reduce** (``fields``)

        Limit a dataframe to some columns

    **report** (``df=None``)

        Returns a dataframe profiling report to print in notebooks

    **resample** (``time_unit='1Min'``, ``date_field=None``)

        Resample the main dataframe to a time period

    **set** (``df``)

        Set a main dataframe

    **to_int** (``fieldname``)

        Convert a column values to integers

