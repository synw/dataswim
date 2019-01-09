Conventions
===========

All functions that end with an underscore return an object. You can often see the same functions
with and without underscore: ex:

This sets a datetime index from a column in the main dataframe:

.. highlight:: python

::

   ds.dateindex("date")
   
This returns a new instance with a dataframe set with a datetime index:

.. highlight:: python

::

   ds2 = ds.dateindex_("date")
   
   
Note: some functions without underscore can still return something: ex: ``ds.show()``
returns a dataframe's head