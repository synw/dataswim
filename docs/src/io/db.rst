Database operations
===================

All operations available for databases. Supported databases: all that SqlAlchemy support

Connect
-------

.. automethod:: dataswim.db.Db.connect

Load data
---------

.. automethod:: dataswim.db.Db.load

.. automethod:: dataswim.db.Db.load_django

.. automethod:: dataswim.db.Db.load_django_
    
Infos
-----

.. automethod:: dataswim.db.Db.tables

.. automethod:: dataswim.db.Db.tables_
    
.. automethod:: dataswim.db.Db.table
    
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
    

InfluxDb
--------

**influx_init** (``url``, ``port``, ``user``, ``pwd``, ``db``)

    Initialize an Influxdb database client
    
**influx_to_csv** (``measurement``, ``batch_size=5000``)

    Batch export data from an Influxdb measurement to csv



    