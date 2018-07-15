from .test_init import TestDsDataInit
from .test_count import TestDsDataCount
from .test_clean import TestDsDataClean
from .test_search import TestDsDataSearch
from .test_select import TestDsDataSelect
from .test_text import TestDsDataText
from .test_stats import TestDsDataStats


#class TestDsData(TestDsDataInit, TestDsDataCount, TestDsDataClean,
#                 TestDsDataSearch, TestDsDataSelect, TestDsDataText):
class TestDsData(TestDsDataClean):
    pass
