from Modules.app import Deposit


class DepositRepo:
    def __init__(self, session):
        self.session = session

    def save(self, deposit):
        self.session.add(deposit)
        self.session.commit()

    def find_by_id(self, deposit_id):
        return self.session.query(Deposit).get(deposit_id)

    def find_all_deposits_by_account_id(self, account_id):
        return self.session.query(Deposit).filter_by(account_id=account_id).all()

    def delete_by_id(self, deposit_id):
        deposit = self.find_by_id(deposit_id)
        if deposit:
            self.session.delete(deposit)
            self.session.commit()