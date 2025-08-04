import pytest
from decimal import Decimal
from banking.interest_rule import InterestRule

def test_valid_interest_rule():
    rule = InterestRule("20230615", "RULE01", Decimal("2.5"))
    assert rule.date == "20230615"
    assert rule.rate == Decimal("2.5")

def test_invalid_date_format():
    with pytest.raises(ValueError):
        InterestRule("2023-06-15", "RULE02", Decimal("1.5"))

def test_invalid_interest_rate_low():
    with pytest.raises(ValueError):
        InterestRule("20230615", "RULE03", Decimal("0"))

def test_invalid_interest_rate_high():
    with pytest.raises(ValueError):
        InterestRule("20230615", "RULE04", Decimal("150.0"))
