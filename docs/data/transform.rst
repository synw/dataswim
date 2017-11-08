Transform data
==============

Columns
-------

**add** (``field``, ``value``)

    Add a columns with default values
    
**drop** (``field``)

    Drops a column from the main dataframe
    
**reduce** (``fields``)

    Limit the main dataframe to some columns
    
**get_reduce** (``fields``)

    Returns a dataframe limited to some columns from the main dataframe
    
**index_col** (``field="date"``)

    Add a column from the index
    
Rows
----
    
**revert** ()

    Reverts the main dataframe order
    
Resample
--------
    
**resample** (``time_period='1Min'``)

    Returns a resampled dataframe from the main dataframe to a time period
    
**rsum** (``time_period="1Min"``)

    Resample and sum the main dataframe to a time period
    
**rsum_** (``time_period="1Min"``)

    Returns a resampled and sumed dataframe from the main dataframe to a time period
    
**apply** (``function``)

    Apply a function on columns values
    
Dataframes
----------

**concat** (``dfs``)

    Concatenate dataframes from a list and set it to the main dataframe

    
