import pytest
from buggy_code import calculate_sum, divide

def test_calculate_sum():
    assert calculate_sum(5, 3) == 8
    assert calculate_sum(0, 0) == 0

def test_divide():
    assert divide(10, 2) == 5
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)