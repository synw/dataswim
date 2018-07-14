from .test_init import TestDsDataInit
from .test_count import TestDsDataCount
from .test_clean import TestDsDataClean
from .test_search import TestDsDataSearch
from .test_select import TestDsDataSelect


#class TestDsData(TestDsDataInit, TestDsDataCount, TestDsDataClean,):
class TestDsData(TestDsDataSelect):
    pass
