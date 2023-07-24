from enum import Enum
from typing import Any


class Bill:
    class BillStatus(Enum):
        PENDING = "Pending"
        CANCELLED = "Cancelled"
        COMPLETED = "Completed"
        RECURRING = "Recurring"

    def __init__(self, id: Any, payee: str, bill_status: 'Bill.BillStatus', nick_name: str, payment_amount: float):
        self.id = int(id)
        self.payee = payee
        self.bill_status = bill_status
        self.nick_name = nick_name
        self.payment_amount = float(payment_amount)
