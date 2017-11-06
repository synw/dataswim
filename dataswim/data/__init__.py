# -*- coding: utf-8 -*-

import pandas as pd
from .views import View
from .clean import Clean
from .count import Count
from .select import Select
from .transform import Transform


class Df(Select, View, Transform, Clean, Count):
    """
    Class for manipulating dataframes
    """

    def __init__(self, df=None):
        """
        Initialize with an empty dataframe
        """
        self.df = df
        self.backup_df = df

    def set(self, df):
        """
        Set a main dataframe
        """
        self.df = df.copy()

    def backup(self):
        """
        Backup the main dataframe
        """
        self.backup_df = self.df.copy()

    def restore(self):
        """
        Restore the main dataframe
        """
        self.df = self.backup_df

    def csv(self, path):
        """
        Saves the main dataframe to a csv file
        """
        self.df.to_csv(path, encoding='utf-8')

    def load_csv(self, url):
        """
        Initialize the main dataframe from csv data
        """
        self.df = pd.read_csv(url)
