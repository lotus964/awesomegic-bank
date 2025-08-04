import pytest
from decimal import Decimal
from banking.transaction import Transaction

def test_valid_transaction():
    txn = Transaction("20230626", "20230626-01", "D", Decimal("100.00"))
    assert txn.txn_type == "D"

def test_invalid_date_format():
    with pytest.raises(ValueError):
        Transaction("26-06-2023", "20230626-01", "D", Decimal("100.00"))

def test_invalid_txn_type():
    with pytest.raises(ValueError):
        Transaction("20230626", "20230626-01", "X", Decimal("100.00"))

def test_negative_amount():
    with pytest.raises(ValueError):
        Transaction("20230626", "20230626-01", "D", Decimal("-10.00"))
