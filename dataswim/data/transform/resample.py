class Resample():
    """
    A class to resample timeseries
    """

    def rsum(self, time_period: str, num_col: str="Number",
             dateindex: str=None):
        """
        Resample and add a sum the main dataframe to a time period

        :param time_period: unit + period: periods are Y, M, D, H, Min, S
        :param time_period: str
        :param num_col: number of the new column, defaults to "Number"
        :param num_col: str, optional
        :param dateindex: column name to use as date index, defaults to None
        :param dateindex: str, optional

        :example: ``ds.rsum("1D")``
        """
        try:
            df = self._resample_("sum", time_period,
                                 num_col, dateindex)
            self.df = df
            if df is None:
                self.err("Can not sum data")
        except Exception as e:
            self.err(e, "Can not sum data")

    def rmean(self, time_period: str, num_col: str="Number",
              dateindex: str=None):
        """
        Resample and add a mean column the main dataframe to a time period

        :param time_period: unit + period: periods are Y, M, D, H, Min, S
        :param time_period: str
        :param num_col: number of the new column, defaults to "Number"
        :param num_col: str, optional
        :param dateindex: column name to use as date index, defaults to None

        :example: ``ds.rmean("1Min")``
        """
        try:
            self.df = self._resample_("mean", time_period,
                                      num_col, dateindex)
        except Exception as e:
            self.err(e, "Can not sum data")

    def _resample_(self, method: str, time_period: str, num_col: str,
                   dateindex: str=None):
        try:
            ds2 = self._duplicate_()
            if dateindex is not None:
                ds2 = self.dateindex_(dateindex)
                if ds2 is None:
                    self.err("Can not process date index")
                    return
            ds2.add(num_col, 1)
            ds2.df = ds2.df.resample(time_period)
            if method == "sum":
                ds2.df = ds2.df.sum()
            elif method == "mean":
                num_vals = ds2.df[num_col].sum()
                ds2.df = ds2.df.mean()
                ds2.df[num_col] = num_vals
            else:
                self.err("Resampling method " + method + " unknown")
                return
            self.ok("Data resampled by", time_period)
            return ds2.df
        except Exception as e:
            self.err(e, "Can not resample data")
