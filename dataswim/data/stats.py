# -*- coding: utf-8 -*
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
