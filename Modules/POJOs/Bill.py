from typing import Any


class Bill:
    def __init__(self, id: Any, payee: str, BillStatus: str, nickName: str, paymentAmount: float):
        self.id = int(id)
        self.payee = payee
        self.BillStatus = BillStatus
        self.nickName = nickName
        self.paymentAmount = float(paymentAmount)
