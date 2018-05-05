# -*- coding: utf-8 -*
import numpy as np
from sklearn import linear_model


class Stats():

    def lreg(self, xcol, ycol, name="regression"):
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
            self.err(e, self.lreg, "Can not calculate linear regression")

    def cvar_(self, col):
        """
        Returns the coefficient of variance of a column
        """
        try:
            v = np.var(self.df[col]), np.std(
                self.df[col]) / np.mean(self.df[col])
            return v[1]
        except Exception as e:
            self.err(
                e,
                self.lreg,
                "Can not calculate coefficient of variation")
