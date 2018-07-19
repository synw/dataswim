from .test_init import TestDsDataInit
from .test_count import TestDsDataCount
from .test_clean import TestDsDataClean
from .test_search import TestDsDataSearch
from .test_select import TestDsDataSelect
from .test_text import TestDsDataText
from .test_stats import TestDsDataStats
from .test_transform import TestDsDataTransform


"""class TestDsData(TestDsDataInit, TestDsDataCount, TestDsDataClean,
                 TestDsDataSearch, TestDsDataSelect, TestDsDataText,
                    TestDsDataStats):
    pass"""
class TestDsData(TestDsDataTransform):
    pass
