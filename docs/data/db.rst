Database operations
===================

Basic operations
----------------

**connect** (``url``)

    Connect to the database and set it as main database
    
**load** (``table``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Set the main dataframe from a table’s data
    
**load_** (``table``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Returns a DataSwim instance from a table's data

**load_django** (``query``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Set a main dataframe from a django orm query
    
**load_django_** (``query``, ``dateindex=None``, ``index_col=None``, ``fill_col=None``)

    Returns a DataSwim instance from a django orm query
    
**insert** (``table``, ``records``, ``create_cols=True``)

    Insert one or many records in the database from a dictionary or a list of dictionaries
    
Infos
-----
    
**tables** (``name=None``, ``p=True``)

    Print existing tables in a database
    
**tables_** (``name=None``, ``p=True``)

    Returns existing tables in a database
    
**table** (``t=None``, ``p=True``)

    Display info about a table

**count_rows** (``name``, ``p=True``)

    Count rows for a table

Select
------

**getall** (``table``)

    Get all rows values for a table
    
Insert
------

**to_db** (``table``, ``db_url=None``)

    Save the main dataframe to the database
    
**update_db** (``table``, ``keys=['id']``, ``db_url=None``)

    Update records in a database table from the main dataframe
    
**insert** (``table``, ``records``, ``create_cols=True``)

    Insert one or many records in the database from a dictionary or a list of dictionaries


Relations
---------

**relation** (``search_ds``, ``origin_field``, ``search_field``, ``destination_field=None``, ``id_field="id"``):

    Add a column to the main dataframe from a relation foreign key 

**relation_** (``search_ds``, ``origin_field``, ``search_field``, ``destination_field=None``, ``id_field="id"``):

    Returns a DataSwim instance with a column filled from a relation foreign key
    



    