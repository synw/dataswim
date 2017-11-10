# -*- coding: utf-8 -*-

import pandas as pd
from .views import View
from .clean import Clean
from .count import Count
from .select import Select
from .transform import Transform
from .export import Export


class Df(Select, View, Transform, Clean, Count, Export):
    """
    Class for manipulating dataframes
    """

    pass
