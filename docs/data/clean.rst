Clean data
==========

Nulls
-----

**drop_nan** (``field=None`` ``method="all``)

    Drop NaN values from the main dataframe
    
**nan_empty** (``field``)

    Fill empty values with NaN values
    
**zero_nan** (``*fields``)

    Converts zero values to nan values in selected columns
    
**zero_nan_** (``*fields``)

    Returns a DataSwim instance with zero values to nan values in selected columns
    
**fill_nan** (``val``, ``*fields``)

    Fill NaN values with new values
    
**fill_nan_** (``val``, ``*fields``)

    Returns a DataSwim instance with NaN values filled
    
**fill_nulls** (``field``)

    Fill all null values with NaN values
    
Numbers
-------
    
**to_int** (``fields``)

    Convert some columns values to integers
    
**to_float** (``*cols``)

    Convert colums values to float
    
Timeseries
----------

**dateindex** (``datafield``, ``indexfield="date_index"``)

    Set a datetime index from a column
    
**dateindex_** (``datafield``, ``indexfield="date_index"``)

    Returns a datetime index from a column
    
**date** (``*fields``)

    Convert column values to datetime from either a list of column names or a single column name string
    
**clean_ts** (``date_col``, ``numeric_col=None``, ``index=True``, ``to_int=False``, ``index_col=True``)

    Cleans and format a timeseries dataframe
    
Cleaning
--------

**transform_** (``dateindex=None``, ``index_col=None``, ``fill_col=None``, ``num_col=None``, ``df=None``)

    Returns a DataSwim instance transformed according to the given parameters
    
