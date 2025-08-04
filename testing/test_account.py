import pytest
from decimal import Decimal
from banking.account import Account
from banking.transaction import Transaction

def test_add_deposit_transaction():
    account = Account("AC001")
    txn = account.add_transaction("20230626", "D", Decimal("100.00"))
    assert txn.txn_type == 'D'
    assert account.balance == Decimal("100.00")

def test_add_withdrawal_transaction():
    account = Account("AC001")
    account.add_transaction("20230625", "D", Decimal("200.00"))
    txn = account.add_transaction("20230626", "W", Decimal("50.00"))
    assert txn.txn_type == 'W'
    assert account.balance == Decimal("150.00")

def test_withdrawal_without_deposit_raises_error():
    account = Account("AC001")
    with pytest.raises(ValueError):
        account.add_transaction("20230626", "W", Decimal("100.00"))

def test_transaction_id_sequence():
    account = Account("AC001")
    t1 = account.add_transaction("20230626", "D", Decimal("10.00"))
    t2 = account.add_transaction("20230626", "D", Decimal("20.00"))
    assert t1.txn_id == "20230626-01"
    assert t2.txn_id == "20230626-02"

def test_get_statement_for_month():
    account = Account("AC001")
    account.add_transaction("20230601", "D", Decimal("100.00"))
    account.add_transaction("20230615", "W", Decimal("30.00"))
    account.add_transaction("20230701", "D", Decimal("50.00"))
    june_txns = account.get_statement("202306")
    assert len(june_txns) == 2

def test_add_interest():
    account = Account("AC001")
    account.add_transaction("20230601", "D", Decimal("100.00"))
    txn = account.add_interest("20230630", Decimal("0.39"))
    assert txn.txn_type == "I"
    assert account.balance == Decimal("100.39")
