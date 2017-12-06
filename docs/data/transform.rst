Transform data
==============

Columns
-------

**add** (``field``, ``value``)

    Add a columns with default values
    
**drop** (``field``)

    Drops a column from the main dataframe
    
**keep** (``fields``)

    Limit the main dataframe to some columns
    
**keep_** (``fields``)

    Returns a dataframe limited to some columns from the main dataframe
    
**index_col** (``field="date"``)

    Add a column filled from the index to the main dataframe
    
**index_col_** (``field="date"``)

    Returns a DatasWim instance with a new column filled from the index
    
**exclude** (``col``, ``val``)

    Delete rows based on value
    
Rows
----
    
**reverse** ()

    Reverse the main dataframe order
    
**sum_** (``column``)

    Returns the sum of all values in a column
    
**sort** (``column``)

    Sorts the main dataframe according to the given column
    
**apply** (``function``)

    Apply a function on columns values
    
Resample
--------
    
**rsum** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Resample and sum the main dataframe to a time period
    
**rsum_** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Returns a resampled and sumed dataframe from the main dataframe to a time period
    
**rmean** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Resample and mean the main dataframe to a time period
    
**rmean_** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Returns a resampled and meaned dataframe from the main dataframe to a time period
    
Dataframes
----------

**concat** (``*dfs``)

    Concatenate dataframes from a list and set it to the main dataframe
    
**concat_** (``*dfs``)

    Concatenate dataframes from a list and returns a DataSwim instance
    
**split_** (``*col``)

    Split the main dataframe according to column values

    
