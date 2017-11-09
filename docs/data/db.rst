Database operations
===================

Basic operations
----------------

**connect** (``url``)

    Connect to the database and set it as main database
    
**load** (``table``)

    Set the main dataframe from a table’s data
    
**load_** (``table``)

    Returns a DataSwim instance from a table's data

**load_django** (``query``)

    Set a main dataframe from a django orm query
    
**load_django_** (``query``)

    Returns a DataSwim instance from a django orm query
    
**insert** (``table``, ``records``, ``create_cols=True``)

    Insert one or many records in the database from a dictionary or a list of dictionaries
    
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

    Returns a DataSwim instance with a column filled from a relation foreign key
    
Import data
-----------

**to_db** (``table``, ``db_url=None``)

    Save the main dataframe to the database


    