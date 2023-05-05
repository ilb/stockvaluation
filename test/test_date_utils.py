from ..date_utils import DateUtils

def test_date_range():
    date_utils = DateUtils()
    range = date_utils.date_range("2020-02-01", -1)
    assert all(range == ["2020-01-31 00:00:00", "2020-02-01 00:00:00"])