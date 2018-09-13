# -*- coding: utf-8 -*
import numpy as np
from sklearn import linear_model


class Stats():

    def lreg(self, xcol, ycol, name="Regression"):
        """
        Add a column to the main dataframe populted with
        the model's linear regression for a column
        """
        try:
            x = self.df[xcol].values.reshape(-1, 1)
            y = self.df[ycol]
            lm = linear_model.LinearRegression()
            lm.fit(x, y)
            predictions = lm.predict(x)
            self.df[name] = predictions
        except Exception as e:
            self.err(e, "Can not calculate linear regression")

    def cvar_(self, col):
        """
        Returns the coefficient of variance of a column
        in percentage
        """
        try:
            v = (np.std(self.df[col]) / np.mean(self.df[col])) * 100
            return v
        except Exception as e:
            self.err(e,
                     "Can not calculate coefficient of variance")
