from dataclasses import dataclass
from decimal import Decimal
import re

@dataclass
class InterestRule:
    date: str      # YYYYMMdd
    rule_id: str
    rate: Decimal  # percent >0 and <100

    def __post_init__(self):
        if not re.match(r"^\d{8}$", self.date):
            raise ValueError(f"Invalid date format: {self.date}")
        if not (Decimal('0') < self.rate < Decimal('100')):
            raise ValueError(f"Interest rate must be >0 and <100, got {self.rate}")
