from typing import Dict, List, Optional, Tuple
from decimal import Decimal, ROUND_HALF_UP
from banking.account import Account
from banking.interest_rule import InterestRule
from banking.transaction import Transaction
import bisect
import datetime

class Bank:
    """
    Manages multiple accounts and interest rules.
    Supports adding transactions, defining interest rules,
    and calculating monthly interest.
    """

    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.interest_rules: List[InterestRule] = []  # Sorted by date ascending

    def _find_or_create_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            self.accounts[account_id] = Account(account_id)
        return self.accounts[account_id]

    def add_transaction(self, date: str, account_id: str, txn_type: str, amount: Decimal) -> Transaction:
        account = self._find_or_create_account(account_id)
        txn = account.add_transaction(date, txn_type, amount)
        return txn

    def add_interest_rule(self, date: str, rule_id: str, rate: Decimal):
        """
        Adds or replaces interest rule for the date.
        """
        # Validate rule inputs done in InterestRule class
        new_rule = InterestRule(date=date, rule_id=rule_id, rate=rate)

        # Remove existing rule on same date if any
        idx = next((i for i, r in enumerate(self.interest_rules) if r.date == date), None)
        if idx is not None:
            self.interest_rules[idx] = new_rule
        else:
            # Insert in sorted order by date
            bisect.insort(self.interest_rules, new_rule, key=lambda r: r.date)

        # Sort again by date just in case
        self.interest_rules.sort(key=lambda r: r.date)

    def get_interest_rules(self) -> List[InterestRule]:
        return self.interest_rules.copy()

    def get_interest_rule_for_date(self, date: str) -> Optional[InterestRule]:
        """
        Returns the interest rule that applies on the given date.
        The latest rule with date <= given date.
        """
        applicable = [rule for rule in self.interest_rules if rule.date <= date]
        if not applicable:
            return None
        return applicable[-1]

    def calculate_monthly_interest(self, account_id: str, year_month: str) -> Tuple[List[Transaction], Decimal]:
        """
        Calculates monthly interest for given account and month.
        Returns list of interest transactions (usually one) and total interest amount.
        """
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")

        account = self.accounts[account_id]
        year = int(year_month[:4])
        month = int(year_month[4:6])

        # Get all days in month
        start_date = datetime.date(year, month, 1)
        if month == 12:
            end_date = datetime.date(year + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(year, month + 1, 1) - datetime.timedelta(days=1)

        total_interest = Decimal('0.00')
        # We'll find continuous periods where interest rate applies and balance is constant

        # Get all transaction dates (sorted) in the account
        tx_dates = account.get_all_transaction_dates()
        # Filter only those within or before this month
        tx_dates = [d for d in tx_dates if d <= end_date.strftime("%Y%m%d")]

        # We use a timeline of dates to determine balance and applicable rule segments
        # We'll add start_date and end_date if not in tx_dates for completeness
        dates = sorted(set([start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")] + tx_dates))

        # Build periods between dates
        periods = []
        for i in range(len(dates)-1):
            period_start = dates[i]
            period_end = (datetime.datetime.strptime(dates[i+1], "%Y%m%d") - datetime.timedelta(days=1)).strftime("%Y%m%d")
            if period_end < period_start:
                continue
            periods.append((period_start, period_end))

        # For the last date itself if not covered
        if dates[-1] == end_date.strftime("%Y%m%d"):
            periods.append((dates[-1], dates[-1]))

        for period_start, period_end in periods:
            # Number of days in period inclusive
            dt_start = datetime.datetime.strptime(period_start, "%Y%m%d").date()
            dt_end = datetime.datetime.strptime(period_end, "%Y%m%d").date()
            num_days = (dt_end - dt_start).days + 1
            if num_days <= 0:
                continue

            # Balance at start of period
            balance = account.get_balance_on_date(period_start)
            # Applicable interest rule at period start
            rule = self.get_interest_rule_for_date(period_start)

            if rule is None:
                continue  # no interest if no rule

            # Interest calculation: balance * rate% * days / 365
            # rate is percent
            interest = (balance * (rule.rate / Decimal('100')) * Decimal(num_days)) / Decimal('365')
            interest = interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            total_interest += interest

        total_interest = total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if total_interest > 0:
            # Credit interest on last day of month
            interest_txn = account.add_interest(end_date.strftime("%Y%m%d"), total_interest)
            return [interest_txn], total_interest
        else:
            return [], Decimal('0.00')

    def get_account_statement(self, account_id: str, year_month: str) -> List[Transaction]:
        """
        Returns all transactions including interest for the specified account and month.
        """
        if account_id not in self.accounts:
            raise ValueError(f"Account {account_id} not found")
        account = self.accounts[account_id]
        return account.get_statement(year_month)
