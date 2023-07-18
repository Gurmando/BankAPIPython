class DepositService:
    def __init__(self, deposit_repo, account_repo):
        self.deposit_repo = deposit_repo
        self.account_repo = account_repo

    def create_deposit(self, account_id, deposit_to_be_created):
        account = self.account_repo.find_by_id(account_id)

        if not account:
            raise ResourceNotFoundException(f"The account with id {account_id} does not exist :(")

        account.balance += deposit_to_be_created.amount
        self.account_repo.save(account)
        deposit_to_be_created.account = account
        self.deposit_repo.save(deposit_to_be_created)

    def get_deposit_by_id(self, deposit_id):
        return self.deposit_repo.find_by_id(deposit_id)

    def get_deposits_for_account(self, account_id):
        return self.deposit_repo.find_all_deposits_by_account_id(account_id)

    def update_deposit(self, deposit_id, deposit_update):
        original_deposit = self.deposit_repo.find_by_id(deposit_id)

        if not original_deposit:
            raise ResourceNotFoundException(f"The original deposit with id {deposit_id} does not exist :(")

        account = original_deposit.account

        if deposit_update.amount != original_deposit.amount:
            account.balance -= original_deposit.amount
            account.balance += deposit_update.amount
            original_deposit.amount = deposit_update.amount
            self.account_repo.save(account)

        if deposit_update.type is not None:
            original_deposit.type = deposit_update.type
        if deposit_update.transaction_date is not None:
            original_deposit.transaction_date = deposit_update.transaction_date
        if deposit_update.status is not None:
            original_deposit.status = deposit_update.status
        if deposit_update.payee_id is not None:
            original_deposit.payee_id = deposit_update.payee_id
        if deposit_update.medium is not None:
            original_deposit.medium = deposit_update.medium
        if deposit_update.description is not None:
            original_deposit.description = deposit_update.description

        self.deposit_repo.save(original_deposit)

    def delete_deposit(self, deposit_id):
        original_deposit = self.deposit_repo.find_by_id(deposit_id)

        if not original_deposit:
            raise ResourceNotFoundException(f"The deposit with an ID of #{deposit_id} does not exist :(")

        account = original_deposit.account
        account.balance -= original_deposit.amount
        self.deposit_repo.delete_by_id(deposit_id)