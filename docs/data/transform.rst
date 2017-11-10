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
    
Rows
----
    
**revert** ()

    Reverts the main dataframe order
    
Resample
--------
    
**resample_** (``time_period='1Min'``, ``index_col=True``, ``fill_col=None``)

    Returns a resampled dataframe from the main dataframe to a time period
    
**rsum** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Resample and sum the main dataframe to a time period
    
**rsum_** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Returns a resampled and sumed dataframe from the main dataframe to a time period
    
**rmean** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Resample and mean the main dataframe to a time period
    
**rmean_** (``time_period="1Min"``, ``index_col=True``, ``fill_col=None``)

    Returns a resampled and meaned dataframe from the main dataframe to a time period
    
**apply** (``function``)

    Apply a function on columns values
    
Dataframes
----------

**concat** (``*dfs``)

    Concatenate dataframes from a list and set it to the main dataframe

    
