# Dataswim

A simple api to clean, transform and visualize data. This api is:

- **Minimalistic**: short names, simple functionalites, minimal parameters
- **Pragmatic**: focuses on raw efficiency rather than idiomatic code
- **Simple stupid**: keep it easy to understand for both code and api

## Dependencies

[Pandas](https://github.com/pandas-dev/pandas) to work with data

[Dataset](https://dataset.readthedocs.io/en/latest/) and [Sql Alchemy](http://www.sqlalchemy.org) to work with databases

To chart data:

- [Bokeh](https://bokeh.pydata.org/en/latest/) with [Holoviews](http://holoviews.org/), 
- [Vega Lite](https://vega.github.io/vega-lite/) with [Altair](https://altair-viz.github.io/) 
- [Seaborn](http://seaborn.pydata.org)
- [Chartjs](http://www.chartjs.org/)

## Supported databases

- Postgresql, Sqlite and all those that Sql Alchemy supports
- Influxdb

## Install 

Using conda:

   ```
   conda install pandas sqlalchemy seaborn
   conda install -c ioam holoviews bokeh
   conda install altair --channel conda-forge
   pip install dataset pandas-profiling pytablewriter goerr gencharts chartjspy
   pip install dataswim --no-deps
   ```

Using pip:

   ```
   pip install dataswim
   ```

To get the Altair charts in notebooks running this command is required:

   ```
   jupyter nbextension enable vega --py --sys-prefix
   ```

## Usage

Read the [api documentation](http://dataswim.readthedocs.io/en/latest/index.html). 

Note: the api may change and is not stable yet. The doc is in sync with master. To autobuild the docs for your
installed version clone and:

   ```
   pip install sphinx
   
   cd docs
   make html
   firefox _build/html/api_auto.html&
   ``` 

## Example

[Jupyter demo notebooks](https://github.com/synw/dataswim-notebooks) are available as example. 

**Users demo notebook**: it uses Django user data loaded from csv or directly from a 
database. Note: the data in this demo is autogenerated and fake but it is possible to run it on real user data
connecting to a Django database.

**Resample data demo**: demonstrates how to resample data by time periods

To run the notebooks online click the 
badge: [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/synw/dataswim-notebooks/master)

### User registrations demo notebook: 

Goal: chart user registrations over time from fake Django user data

```python
from dataswim import ds

# Load from a Django database
#ds.connect('postgresql://user:xxxx@localhost/dbname')
#ds.connect('sqlite:////path/to/db.sqlite3')
#ds.load("auth_user")

# Load demo data from csv
ds.load_csv("data/users.csv")

# for a full report (very small datasets only):
#ds.report()
# for a data description:
#ds.describe()
# for a quick look:
#ds.look()
# for a sample:
ds.show()
```

    [START] Loading csv...
    [END] Finished loading csv in 0.12 seconds
    [INFO] The dataframe has 1007 rows and 11 columns:
    id, password, last_login, is_superuser, first_name, last_name, email, is_staff, is_active, 
    date_joined, username

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>password</th>
      <th>last_login</th>
      <th>is_superuser</th>
      <th>first_name</th>
      <th>last_name</th>
      <th>email</th>
      <th>is_staff</th>
      <th>is_active</th>
      <th>date_joined</th>
      <th>username</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>pbkdf2_sha256$36000$TGjJvvfpuFhR$jVD3mP8MNxNYD...</td>
      <td>2017-12-02 14:05:30.796573</td>
      <td>True</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>True</td>
      <td>True</td>
      <td>2017-12-02 13:57:53.393755</td>
      <td>ggg</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>Cupiditate accusamus velit sit dolor. Doloribu...</td>
      <td>1986-07-16 11:22:02.000000</td>
      <td>False</td>
      <td>Lindsey</td>
      <td>Thompson</td>
      <td>farmermeghan@henderson.com</td>
      <td>False</td>
      <td>False</td>
      <td>1997-08-06 16:23:37.000000</td>
      <td>jrichards</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>Nobis quisquam voluptatibus nulla.\nEa archite...</td>
      <td>1981-04-06 06:48:03.000000</td>
      <td>False</td>
      <td>Kurt</td>
      <td>Black</td>
      <td>kellycharles@marsh.com</td>
      <td>True</td>
      <td>True</td>
      <td>2013-08-29 18:04:10.000000</td>
      <td>eroberts</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>Inventore ea quia ducimus eligendi quod. Velit...</td>
      <td>1991-08-08 22:23:45.000000</td>
      <td>True</td>
      <td>Sandra</td>
      <td>Wilson</td>
      <td>antoniobowers@hotmail.com</td>
      <td>True</td>
      <td>False</td>
      <td>1981-04-22 05:32:55.000000</td>
      <td>emilykelley</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>Veniam sequi aut nisi vitae. Quasi explicabo v...</td>
      <td>1971-02-08 15:53:42.000000</td>
      <td>True</td>
      <td>Andrew</td>
      <td>Guzman</td>
      <td>hannahconner@yahoo.com</td>
      <td>False</td>
      <td>False</td>
      <td>2010-11-10 17:53:54.000000</td>
      <td>lsmith</td>
    </tr>
  </tbody>
</table>
</div>

## Transform the data


```python
# Resample data by one year
# see Pandas frequencies for units: 
# https://github.com/pandas-dev/pandas/blob/master/pandas/tseries/frequencies.py#L98
# try "1D" for one day
ds.rsum("1A", dateindex="date_joined", num_col="Registrations", index_col="Date")
# Convert nulls to zeros
ds.zero_nan("Registrations")
# Keep only the fields we need
ds.keep("Date", "Registrations")
ds.backup()
ds.show()
```

    [OK] Added a datetime index from column date_joined
    [OK] Data resampled by 1A
    [OK] Column Date added from index
    [OK] Replaced 0 values by nan in column Registrations
    [OK] Setting dataframe to columns Date Registrations
    [OK] Dataframe backed up
    [INFO] The dataframe has 48 rows and 2 columns:
    Date, Registrations

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Date</th>
      <th>Registrations</th>
    </tr>
    <tr>
      <th>date_joined</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1970-12-31</th>
      <td>1970-12-31</td>
      <td>20</td>
    </tr>
    <tr>
      <th>1971-12-31</th>
      <td>1971-12-31</td>
      <td>21</td>
    </tr>
    <tr>
      <th>1972-12-31</th>
      <td>1972-12-31</td>
      <td>20</td>
    </tr>
    <tr>
      <th>1973-12-31</th>
      <td>1973-12-31</td>
      <td>25</td>
    </tr>
    <tr>
      <th>1974-12-31</th>
      <td>1974-12-31</td>
      <td>26</td>
    </tr>
  </tbody>
</table>
</div>

## Draw charts

```python
import holoviews as hv
hv.extension('bokeh')
```
### Simple line

```python
ds.chart("Date", "Registrations", label="Registrations")
ds.line_()
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/line.png)

### Line and points

```python
ds.opts(dict(width=940, height=300))
line = ds.line_()
style = dict(color="orange", size=10)
opts = dict(tools=["hover"])
point = ds.point_(style=style, opts=opts)
# The * operator merge the two charts in one
line*point
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/line_point.png)

### Different types of chart

```python
ds.width(300)
ds.height(200)
ds.color("orange")
area = ds.area_()
ds.color("green")
point = ds.point_()
ds.color("grey")
bar = ds.bar_()
area+point+bar
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/multi.png)

### Histogram and mean line

```python
ds.color("green")
ds.width(850)
ds.height(300)
c7 = ds.hline_("Registrations")
c8 = ds.area_("Registrations").hist()
c8*c7
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/hist.png)

### Linear regression with marginal distributions

Convert all to integers for the plot to work

```python
ds.to_int("Date")
ds.to_int("Registrations")
```

Draw the chart

```python
% matplotlib inline
ds.opts(dict(xticks=(1970, 2017), yticks=(0, 35)))
c = ds.linear_()
```

```
    [INFO] Switching to the Seaborn engine to draw this chart
```

![Users chart](https://github.com/synw/dataswim/blob/master/docs/img/linear.png)


