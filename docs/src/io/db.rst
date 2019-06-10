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

.. automethod:: dataswim.db.insert.Insert.to_db

.. automethod:: dataswim.db.insert.Insert.update_table

.. automethod:: dataswim.db.insert.Insert.insert

.. automethod:: dataswim.db.insert.Insert.upsert


Relations
---------

.. automethod:: dataswim.db.relations.Relation.relation

.. automethod:: dataswim.db.relations.Relation.relation_
    

InfluxDb
--------

**influx_init** (``url``, ``port``, ``user``, ``pwd``, ``db``)

    Initialize an Influxdb database client
    
**influx_to_csv** (``measurement``, ``batch_size=5000``)

    Batch export data from an Influxdb measurement to csv



    