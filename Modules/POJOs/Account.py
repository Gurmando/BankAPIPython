class Account:
    def __init__(self, id, account_type, nickname, rewards, balance, customer):
        self.id = int(id)
        self.type = account_type
        self.nickname = str(nickname)
        self.rewards = int(rewards)
        self.balance = float(balance)
        self.customer = customer
