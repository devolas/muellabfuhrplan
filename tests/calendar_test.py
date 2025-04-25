import pytest
import datetime
from ..eins import calcDateTimeBegin


@pytest.fixture
def pickup_fixture():
    resource = [{'id': 461, 'weekday': 'Fr', 'day': '02', 'month': '01', 'year': '2026', 'gelber': 'RW'}, {'id': 462, 'weekday': 'Th', 'day': '01', 'month': '01', 'year': '2026', 'gelber': 'RW', 'bio': 'Gai'}]
    yield resource  # This is the value that will be passed to the test
    # Teardown code: This code runs after the test
    resource.clear()
 

def test_original_functionality(pickup_fixture):
    assert calcDateTimeBegin(pickup_fixture[0]) == datetime.datetime(2026, 1, 2, 0, 0)

def test_offset_plus(pickup_fixture):
    assert calcDateTimeBegin(pickup_fixture[0], 6) == datetime.datetime(2026, 1, 2, 6, 0)

def test_offset_plus_more_than_one_day(pickup_fixture):
    assert calcDateTimeBegin(pickup_fixture[0], 25) == datetime.datetime(2026, 1, 3, 1, 0)

def test_offset_minus_cross_day_boarder(pickup_fixture):
    assert calcDateTimeBegin(pickup_fixture[0], -6) == datetime.datetime(2026, 1, 1, 18, 0)

def test_offset_minus_cross_month_boarder(pickup_fixture):
    assert calcDateTimeBegin(pickup_fixture[1], -5) == datetime.datetime(2025, 12, 31, 19, 0)

if __name__ == '__main__':
    pytest.main()