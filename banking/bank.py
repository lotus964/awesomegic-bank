from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
from banking.account import Account
from banking.interest_rule import InterestRule
from banking.transaction import Transaction
import datetime

class Bank:
    """
    Manages multiple accounts and interest rules.
    Supports adding transactions, defining interest rules,
    and calculating monthly interest.
    """

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.interest_rules: List[InterestRule] = []

    def _find_or_create_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            self.accounts[account_id] = Account(account_id)
        return self.accounts[account_id]

    # Return Transaction or raise Exception (match test expectations)
    def add_transaction(self, date: str, account_id: str, txn_type: str, amount: Decimal) -> Transaction:
        account = self._find_or_create_account(account_id)
        txn = account.add_transaction(date, txn_type, amount)  # may raise ValueError
        return txn

    # Still returning tuple here for status message, can change if needed
    def add_interest_rule(self, date: str, rule_id: str, rate: Decimal) -> Tuple[bool, str]:
        if rate <= 0 or rate >= 100:
            return False, "Rate must be between 0 and 100"

        new_rule = InterestRule(date=date, rule_id=rule_id, rate=rate)

        idx = next((i for i, r in enumerate(self.interest_rules) if r.date == date), None)
        if idx is not None:
            self.interest_rules[idx] = new_rule
        else:
            self.interest_rules.append(new_rule)

        self.interest_rules.sort(key=lambda r: r.date)
        return True, f"Interest rule {rule_id} added for {date} with rate {rate}%"

    def get_interest_rules(self) -> List[InterestRule]:
        return self.interest_rules.copy()

    def get_interest_rule_for_date(self, date: str) -> Optional[InterestRule]:
        applicable = [rule for rule in self.interest_rules if rule.date <= date]
        return applicable[-1] if applicable else None

    def calculate_monthly_interest(self, account_id: str, year_month: str) -> Tuple[List[Transaction], Decimal]:
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")

        account = self.accounts[account_id]
        year = int(year_month[:4])
        month = int(year_month[4:6])

        start_date = datetime.date(year, month, 1)
        end_date = (
            datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
            if month == 12
            else datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)
        )

        total_interest = Decimal('0.00')
        tx_dates = [d for d in account.get_all_transaction_dates() if d <= end_date.strftime("%Y%m%d")]
        dates = sorted(set([start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")] + tx_dates))

        periods = []
        for i in range(len(dates) - 1):
            period_start = dates[i]
            period_end = (datetime.datetime.strptime(dates[i + 1], "%Y%m%d") - datetime.timedelta(days=1)).strftime("%Y%m%d")
            if period_end >= period_start:
                periods.append((period_start, period_end))
        if dates[-1] == end_date.strftime("%Y%m%d"):
            periods.append((dates[-1], dates[-1]))

        for period_start, period_end in periods:
            dt_start = datetime.datetime.strptime(period_start, "%Y%m%d").date()
            dt_end = datetime.datetime.strptime(period_end, "%Y%m%d").date()
            num_days = (dt_end - dt_start).days + 1
            if num_days <= 0:
                continue

            balance = account.get_balance_on_date(period_start)
            rule = self.get_interest_rule_for_date(period_start)
            if not rule:
                continue

            interest = (balance * (rule.rate / Decimal('100')) * Decimal(num_days)) / Decimal('365')
            interest = interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total_interest += interest

        total_interest = total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if total_interest > 0:
            interest_txn = account.add_interest(end_date.strftime("%Y%m%d"), total_interest)
            return [interest_txn], total_interest
        return [], Decimal('0.00')

    def get_account_statement(self, account_id: str, year_month: str) -> List[Transaction]:
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        return self.accounts[account_id].get_statement(year_month)
