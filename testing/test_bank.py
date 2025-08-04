import pytest
from decimal import Decimal
from banking.bank import Bank
from banking.account import Account
from banking.interest_rule import InterestRule
from banking.transaction import Transaction

def test_add_transaction_creates_account():
    bank = Bank()
    txn = bank.add_transaction("20230626", "AC001", "D", Decimal("100.00"))
    assert isinstance(txn, Transaction)
    assert txn.txn_type == 'D'
    assert txn.amount == Decimal("100.00")
    assert "AC001" in bank.accounts
    account = bank.accounts["AC001"]
    assert account.balance == Decimal("100.00")

def test_withdrawal_constraints():
    bank = Bank()
    bank.add_transaction("20230601", "AC001", "D", Decimal("100.00"))
    # Withdrawal greater than balance raises error
    with pytest.raises(ValueError):
        bank.add_transaction("20230626", "AC001", "W", Decimal("150.00"))
    # Withdrawal that does not go below zero works
    txn = bank.add_transaction("20230626", "AC001", "W", Decimal("50.00"))
    assert txn.txn_type == 'W'
    assert bank.accounts["AC001"].balance == Decimal("50.00")

def test_add_interest_rule():
    bank = Bank()
    bank.add_interest_rule("20230615", "RULE01", Decimal("2.5"))
    rules = bank.get_interest_rules()
    assert len(rules) == 1
    assert rules[0].rate == Decimal("2.5")

def test_calculate_monthly_interest():
    bank = Bank()
    bank.add_transaction("20230601", "AC001", "D", Decimal("36500.00"))  # 365 days for 100 units/day interest
    bank.add_interest_rule("20230601", "R1", Decimal("1.0"))  # 1% yearly rate
    interest_txns, interest_amount = bank.calculate_monthly_interest("AC001", "202306")
    # 36500 * 1% * 30 / 365 = 30.00
    assert interest_amount == Decimal("30.00")
    assert len(interest_txns) == 1
    assert interest_txns[0].txn_type == 'I'
    assert interest_txns[0].amount == interest_amount

def test_statement_includes_interest():
    bank = Bank()
    bank.add_transaction("20230601", "AC001", "D", Decimal("100.00"))
    bank.add_interest_rule("20230601", "R1", Decimal("12.0"))  # 12% yearly
    bank.calculate_monthly_interest("AC001", "202306")
    stmts = bank.get_account_statement("AC001", "202306")
    assert any(t.txn_type == 'I' for t in stmts)
