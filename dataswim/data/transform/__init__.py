# @PydevCodeAnalysisIgnore
from .columns import Columns
from .values import Values
from .resample import Resample
from .dataframe import Dataframe
from .calculations import Calculations


class Transform(Columns, Values, Resample, Dataframe, Calculations):
    """
    Class to transform data
    """

    pass
