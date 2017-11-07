Select data
===========

Rows
----

**first** (``main=True``)

    Select the first row
    
**limit** (``r=5``, ``main=True``)

    Limit selection the a range
    
**contains** (``value``, ``field``)

    Returns rows that contains a string value in a column
    
**exact** (``value``, ``field``)

    Returns rows that has the exact string value in a column
    
**range** (``num``, ``unit``)

    Limit the data in a time range
    
Dataframes
----------

**load_csv** (``url``)

    Initialize the main dataframe from csv data
    
**set** (``df``)

    Set a main dataframe
    
**backup** ()

    Backup the main dataframe
    
**restore** ()

    Restore the main dataframe
 