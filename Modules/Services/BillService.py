from typing import Any

from Modules.POJOs.Bill import Bill


class BillService:

    def __init__(self, bill_repo):
        self.bill_repo = bill_repo

    def create_bill(self, id: Any, payee: str, bill_status: str, nick_name: str, payment_amount: float):
        bill = Bill(id, payee, bill_status, nick_name, payment_amount)
        return self.bill_repo.save(bill)

    def get_bill(self, id):
        return self.bill_repo.find_by_id(id)

    def delete_bill(self, id):
        self.bill_repo.delete(id)

    def update_bill(self, id: Any, payee: str = None, bill_status: str = None, nick_name: str = None,
                    payment_amount: float = None):
        bill = self.get_bill(id)
        if bill:
            if payee is not None:
                bill.payee = payee
            if bill_status is not None:
                bill.bill_status = bill_status
            if nick_name is not None:
                bill.nick_name = nick_name
            if payment_amount is not None:
                bill.payment_amount = float(payment_amount)
            self.bill_repo.save(bill)
