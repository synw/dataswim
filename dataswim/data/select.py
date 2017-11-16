import pandas as pd


class Select():
    """
    Class to select data
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df

    def first_(self):
        """
        Returns the first row
        """
        return self._first()

    def _first(self):
        """
        Select the first row
        """
        try:
            val = self.df.iloc[0]
            return val
        except Exception as e:
            self.err(e, self.first, "Can not select first row")

    def limit(self, r=5):
        """
        Limit selection the a range in the main dataframe
        """
        try:
            self.df = self.df[:r]
        except Exception as e:
            self.err(e, self.limit, "Can not limit data")

    def limit_(self, r=5):
        """
        Returns a DataSwim instance with limited selection
        """
        try:
            return self.new(self.df[:r])
        except Exception as e:
            self.err(e)

    def unique_(self, column):
        """
        Returns unique values in a column
        """
        try:
            df = self.df[column].unique()
            return df
        except Exception as e:
            self.err(e, self.unique, "Can not select unique data")

    def range_(self, num, unit):
        """
        Limit the data in a time range
        """
        try:
            df = self.df[self.df.last_valid_index() -
                         pd.DateOffset(num, unit):]
            return self.clone_(df=df)
        except Exception as e:
            self.err(e, self.range_, "Can not select range data")
        return self.duplicate(df)

    def to_records_(self):
        """
        Returns a list of dictionary records from the main dataframe
        """
        try:
            dic = self.df.to_dict(orient="records")
            return dic
        except Exception as e:
            self.err(e, self.to_records_, "Can not create records")

    def nulls_(self, field):
        """
        Return all null rows
        """
        try:
            null_rows = self.df[field][self.df[field].isnull()]
        except Exception as e:
            self.err(e, self.nulls_, "Can not select null rows")
        return null_rows
