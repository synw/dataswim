Database operations
===================

Basic operations
----------------

**connect** (``url``)

    Connect to the database and set it as main database
    
**load** (``table``)

    Set the main dataframe from a table’s data
    
**get_load** (``table``)

    Returns a table's data in a dataframe

**load_django** (``query``)

    Set a main dataframe from a django orm query
    
**get_load_django** (``query``)

    Returns dataframe from a django orm query
    
Queries
-------
    
**tables** (``name=None``, ``p=True``)

    Print existing tables in a database
    
**table** (``t=None``, ``p=True``)

    Display info about a table

**count_rows** (``name``, ``p=True``)

    Count rows for a table

**getall** (``table``)

    Get all rows values for a table

Relations
---------

**relation** (``search_ds``, ``origin_field``, ``search_field``, ``destination_field=None``, ``id_field="id"``):

    Add a column to the main dataframe from a relation foreign key 

**relation_** (``search_ds``, ``origin_field``, ``search_field``, ``destination_field=None``, ``id_field="id"``):

    Returns a dataframe with a column filled from a relation foreign key 



    