Select data
===========

Rows
----

**first** ()

    Select the first row
    
**first_** ()

    Returns the first row
    
**limit** (``r=5``)

    Limit selection the a range in the main dataframe
    
**limit_** (``r=5``)

    Returns a DataSwim instance with limited selection
    
**unique_** (``column``)

    Returns unique values in a column
    
**nulls_** (``field``)

    Return all null rows
    
**to_records_** ()

    Returns a list of dictionary records from the main dataframe
    
**range** (``num``, ``unit``)

    Limit the data in a time range and set the main dataframe
    
**range_** (``num``, ``unit``)

    Limit the data in a time range and returns a DataSwim instance
    
**nowrange** (``col``, ``interval``, ``unit="D"``)

    Set the main dataframe with rows within a date range from now
    
**nowrange_** (``col``, ``interval``, ``unit="D"``)

    Returns a Dataswim instance with rows within a date range from now
    
**contains** (``column``, ``value``)

    Returns rows that contains a string value in a column
    
**exact** (``column``, ``value``)

    Returns rows that has the exact string value in a column
    
Columns
-------

**col_dict_** (``column``, ``key=None``)

    Returns a dictionnary from a column's values
    
Dataframes
----------

**load_csv** (``url``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Initialize the main dataframe from csv data
    
**load_csv_** (``url``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Returns a DataSwim instance from csv data
    
**set** (``df=None``, ``db=None``)

    Set a main dataframe
    
**clone** ()

    Returns a new DataSwim instance from the current instance
    
**duplicate_** (``df=None``, ``db=None``, ``quiet=False``)

    Returns a new DataSwim instance using the previous database connection
    
**backup** ()

    Backup the main dataframe
    
**restore** ()

    Restore the main dataframe
    
**to_records_** ()

    Returns a list of dictionary records from the main dataframe

 