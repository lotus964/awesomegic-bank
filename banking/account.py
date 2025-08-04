from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict
from banking.transaction import Transaction

class Account:
    """
    Represents a bank account with transactions.
    Maintains balance and generates unique transaction IDs.
    """

    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transactions: List[Transaction] = []
        # Map date to count of transactions to generate txn id suffix
        self.txn_counter: Dict[str, int] = {}
        self.balance = Decimal('0.00')

    def _next_txn_id(self, date: str) -> str:
        count = self.txn_counter.get(date, 0) + 1
        self.txn_counter[date] = count
        return f"{date}-{count:02d}"

    def add_transaction(self, date: str, txn_type: str, amount: Decimal) -> Transaction:
        """
        Adds a deposit or withdrawal transaction after validation.
        Updates balance accordingly.
        """
        txn_type = txn_type.upper()
        if txn_type not in {'D', 'W'}:
            raise ValueError("Transaction type must be 'D' or 'W'")

        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")

        if txn_type == 'W':
            if not self.transactions:
                raise ValueError("Cannot withdraw from account with zero balance")
            if self.balance - amount < 0:
                raise ValueError("Withdrawal would cause negative balance")

        txn_id = self._next_txn_id(date)
        txn = Transaction(date=date, txn_id=txn_id, txn_type=txn_type, amount=amount)
        self.transactions.append(txn)

        # Update balance
        if txn_type == 'D':
            self.balance += amount
        else:
            self.balance -= amount

        self.balance = self.balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return txn

    def add_interest(self, date: str, amount: Decimal) -> Transaction:
        """
        Adds interest transaction (type 'I') to the account.
        """
        amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if amount < 0:
            raise ValueError("Interest amount cannot be negative")

        txn_id = ""  # Interest transactions have empty txn_id as per spec
        txn = Transaction(date=date, txn_id=txn_id, txn_type='I', amount=amount)
        self.transactions.append(txn)
        self.balance += amount
        self.balance = self.balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return txn

    def get_statement(self, year_month: str) -> List[Transaction]:
        """
        Returns list of transactions including interest transactions for the specified year-month.
        Date format YYYYMM
        """
        if len(year_month) != 6 or not year_month.isdigit():
            raise ValueError("YearMonth must be in YYYYMM format")

        return [txn for txn in self.transactions if txn.date.startswith(year_month)]

    def get_balance_on_date(self, date: str) -> Decimal:
        """
        Returns balance at the end of a given date.
        Considers all transactions up to and including that date.
        """
        balance = Decimal('0.00')
        for txn in sorted(self.transactions, key=lambda t: (t.date, t.txn_id or "")):
            if txn.date > date:
                break
            if txn.txn_type == 'D' or txn.txn_type == 'I':
                balance += txn.amount
            elif txn.txn_type == 'W':
                balance -= txn.amount
        return balance.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def get_all_transaction_dates(self) -> List[str]:
        """Returns sorted unique transaction dates."""
        dates = sorted(set(txn.date for txn in self.transactions))
        return dates
