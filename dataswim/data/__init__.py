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

    pass
