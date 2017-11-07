Clean data
==========

Nulls
-----

**drop_nan** (``field=None``)

    Drop NaN values from the main dataframe
    
**nan_empty** (``field``)

    Fill empty values with NaN values
    
**fill** (``fields``, ``val=0``)

    Fill NaN values with new values either from a list of columns or a single column name string
    
**fill_nulls** (``field``)

    Fill all null values with NaN values
    
Numbers
-------
    
**to_int** (``fields``)

    Convert a column values to integers either from a list of columns or a single column name string
    
Timeseries
----------

**index** (``datafield``, ``indexfield``)

    Set a datetime index from a column
    
**date** (``fields``)

    Convert column values to datetime from either a list of column names or a single column name string
    
**clean_ts** (``date_col``, ``numeric_col``)

    Cleans and format a timeseries dataframe
    
