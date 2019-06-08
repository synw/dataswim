import pandas as pd
from ..copy import Copy


class Dataframe(Copy):
    """
    Class to transform the dataframe
    """

    def concat(self, *dss, **kwargs):
        """
        Concatenate dataswim instances from and
                set it to the main dataframe

        :param dss: dataswim instances to concatenate
        :type dss: Ds
        :param kwargs: keyword arguments for ``pd.concat``


        """
        try:
            df = pd.DataFrame()
            for dsx in dss:
                df = pd.concat([df, dsx.df], **kwargs)
            self.df = df
        except Exception as e:
            self.err(e, "Can not concatenate data")

    def concat_(self, *dss, **kwargs):
        """
        Concatenate dataswim instances and
                return a new Ds instance

        :param dss: dataswim instances to concatenate
        :type dss: Ds
        :param kwargs: keyword arguments for ``pd.concat``
        :rtype: Ds

        """
        try:
            df = pd.DataFrame()
            for dsx in dss:
                df = pd.concat([df, dsx.df], **kwargs)
            return self.new_(df=df)
        except Exception as e:
            self.err(e, "Can not concatenate data")

    def split_(self, col: str) -> "list(Ds)":
        """
        Split the main dataframe according to a column's unique values and
        return a dict of dataswim instances

        :return: list of dataswim instances
        :rtype: list(Ds)

        :example: ``dss = ds.slit_("Col 1")``
        """
        try:
            dss = {}
            unique = self.df[col].unique()
            for key in unique:
                df2 = self.df.loc[self.df[col] == key]
                ds2 = self._duplicate_(df2)
                dss[key] = ds2
            return dss
        except Exception as e:
            self.err(e, "Can not split dataframe")

    def merge(self, df: pd.DataFrame, on: str, how: str="outer", **kwargs):
        """
        Set the main dataframe from the current dataframe and the passed
        dataframe

        :param df: the pandas dataframe to merge
        :type df: pd.DataFrame
        :param on: param for ``pd.merge``
        :type on: str
        :param how: param for ``pd.merge``, defaults to "outer"
        :type how: str, optional
        :param kwargs: keyword arguments for ``pd.merge``
        """
        try:
            df = pd.merge(self.df, df, on=on, how=how, **kwargs)
            self.df = df
        except Exception as e:
            self.err(e, self.merge, "Can not merge dataframes")
