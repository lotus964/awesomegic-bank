from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
import re

@dataclass(frozen=True)
class Transaction:
    date: str       # YYYYMMdd
    txn_id: str     # Unique ID, e.g. "20230626-01"
    txn_type: str   # 'D' or 'W' or 'I' (interest)
    amount: Decimal # Always positive

    def __post_init__(self):
        if not re.match(r"^\d{8}$", self.date):
            raise ValueError(f"Invalid date format: {self.date}")
        if self.txn_type.upper() not in {'D', 'W', 'I'}:
            raise ValueError(f"Invalid transaction type: {self.txn_type}")
        if self.amount <= 0:
            raise ValueError("Transaction amount must be > 0")

    @staticmethod
    def round_amount(value: Decimal) -> Decimal:
        return value.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
