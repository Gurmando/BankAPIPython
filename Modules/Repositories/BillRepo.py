# from Modules.POJOs.Bill import Bill
#
#
# class BillRepo:
#     def __init__(self, session):
#         self.session = session
#
#     def save(self, bill: Bill):
#         self.session.add(bill)
#         self.session.commit()
#         return bill
#
#     def find_by_id(self, bill_id):
#         return self.session.query(Bill).filter(Bill.id == bill_id).first()
#
#     def find_all_bills_by_account_id(self, account_id):
#         return self.session.query(Bill).filter(Bill.account_id == account_id).all()
#
#     def delete(self, bill_id):
#         bill = self.find_by_id(bill_id)
#         if bill:
#             self.session.delete(bill)
