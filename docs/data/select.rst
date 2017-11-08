Select data
===========

Rows
----

**first** ()

    Select the first row
    
**limit** (``r=5``)

    Limit selection the a range
    
**contains** (``column``, ``value``)

    Returns rows that contains a string value in a column
    
**exact** (``column``, ``value``)

    Returns rows that has the exact string value in a column
    
**filter** (``column``, ``value``)

    Filters the main dataframe based on column value
    
**filter** (``column``, ``value``)

    Returns a DataSwim instance based on column value
    
**range** (``num``, ``unit``)

    Limit the data in a time range
    
Dataframes
----------

**load_csv** (``url``)

    Initialize the main dataframe from csv data
    
**set** (``df=None``, ``db=None``)

    Set a main dataframe
    
**clone** ()

    Returns a new DataSwim instance from the current instance
    
**duplicate** ()

    Returns a new DataSwim instance using the previous database connection
    
**backup** ()

    Backup the main dataframe
    
**restore** ()

    Restore the main dataframe
 