# Dataswim

A simple api to clean, transform and visualize data. This api is:

- **Minimalistic**: short names, simple functionalites, minimal parameters
- **Pragmatic**: focuses on raw efficiency rather than idiomatic code
- **Simple stupid**: keep it easy to understand for both code and api

## Dependencies

[Dataset](https://dataset.readthedocs.io/en/latest/) and [Sql Alchemy](http://www.sqlalchemy.org) to work with databases

[Pandas](https://github.com/pandas-dev/pandas) and 
[Pandas profiling](https://github.com/JosPolfliet/pandas-profiling) to work with data

[Holoviews](http://holoviews.org/) and [Bokeh](https://bokeh.pydata.org/en/latest/) to chart data

   ```
   pip install pandas_profiling dataset
   # and then:
   conda install -c ioam holoviews bokeh
   # or:
   pip install holoviews
   ```

## Usage

Read the [api documentation](http://dataswim.readthedocs.io/en/latest/api.html#database-operations).

Warning: to api documentation might not be up to date as this module is currently under heavy development and
moving fast

## Example

[Jupyter demo notebooks](https://github.com/synw/dataswim-notebooks) are available as example. 

**Users demo notebook**: it uses Django user data loaded from csv or directly from a 
database. Note: the data in this demo is autogenerated and fake but it is possible to run it on real user data
connecting to a Django database.

**Resample data demo**: demonstrates how to resample data by time periods

Run the users demo notebook:

```python
from dataswim import ds

# Load from csv
ds.load_csv("data/users.csv")

# Load from a Django database
#ds.connect('postgresql://user:xxxx@localhost/dbname')
#ds.connect('sqlite:////path/to/db.sqlite3')
#ds.load("auth_user")

# for a full report:
#ds.report()
# for a data description:
#ds.describe()
# for a quick look:
ds.look()
```

    221 rows
    Fields: id, password, last_login, is_superuser, first_name, last_name, email, is_staff, is_active, date_joined, username


### Clean and format the data


```python
# drop null values
ds.drop_nan()
# format date fields
ds.date(["last_login", "date_joined"])
# keep only the relevant data
ds.reduce(["username", "date_joined"])
# print data
ds.show()
```

    221 rows
    Fields: username, date_joined





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>username</th>
      <th>date_joined</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>bob</td>
      <td>2017-10-31 09:24:10</td>
    </tr>
    <tr>
      <th>1</th>
      <td>denise40</td>
      <td>1974-03-15 13:13:54</td>
    </tr>
    <tr>
      <th>2</th>
      <td>hannah55</td>
      <td>2008-03-05 13:25:32</td>
    </tr>
    <tr>
      <th>3</th>
      <td>dbaker</td>
      <td>2017-04-10 19:12:24</td>
    </tr>
    <tr>
      <th>4</th>
      <td>youngnatasha</td>
      <td>1975-01-15 08:02:34</td>
    </tr>
  </tbody>
</table>
</div>



### Transform the data


```python
# Add a num field
ds.add("Logins", 1)
# Create a datetime index
ds.index("date_joined", "Date")
ds.show()
```

    221 rows
    Fields: username, date_joined, Logins





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>username</th>
      <th>date_joined</th>
      <th>Logins</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-10-31 09:24:10</th>
      <td>bob</td>
      <td>2017-10-31 09:24:10</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1974-03-15 13:13:54</th>
      <td>denise40</td>
      <td>1974-03-15 13:13:54</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2008-03-05 13:25:32</th>
      <td>hannah55</td>
      <td>2008-03-05 13:25:32</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2017-04-10 19:12:24</th>
      <td>dbaker</td>
      <td>2017-04-10 19:12:24</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1975-01-15 08:02:34</th>
      <td>youngnatasha</td>
      <td>1975-01-15 08:02:34</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Resample data by one year
# see Pandas frequencies for units: 
# https://github.com/pandas-dev/pandas/blob/master/pandas/tseries/frequencies.py#L98
# try "1D" for 1 day
df = ds.resample("1A").sum()
```


```python
# Set the new data as the main dataset
ds.set(df)
# set nulls to 0
ds.fill("Logins")
# convert floats
ds.to_int("Logins")
# Add a date column from index
ds.date_field("Date")
```


```python
# check it out
ds.show()
```

    48 rows
    Fields: Logins, Date





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Logins</th>
      <th>Date</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1970-12-31</th>
      <td>7</td>
      <td>1970-12-31</td>
    </tr>
    <tr>
      <th>1971-12-31</th>
      <td>4</td>
      <td>1971-12-31</td>
    </tr>
    <tr>
      <th>1972-12-31</th>
      <td>6</td>
      <td>1972-12-31</td>
    </tr>
    <tr>
      <th>1973-12-31</th>
      <td>4</td>
      <td>1973-12-31</td>
    </tr>
    <tr>
      <th>1974-12-31</th>
      <td>6</td>
      <td>1974-12-31</td>
    </tr>
  </tbody>
</table>
</div>



### Draw charts


```python
import holoviews as hv
hv.extension('bokeh')
```

```python
ds.chart("Date", "Logins")
ds.line()
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/line.png)

```python
ds.color("green")
ds.bar()
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/bar.png)

```python
colors=dict(line="orange", point="blue")
ds.line_point(colors)
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/line_point.png)

```python
ds.width(300)
ds.height(180)
ds.color("blue")
line = ds.line()
ds.color("red")
point = ds.point()
ds.color("green")
bar = ds.bar()
point+line+bar
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/multi.png)

