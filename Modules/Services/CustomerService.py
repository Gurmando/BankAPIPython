class CustomerService:
    def __init__(self, customer_repo):
        self.customer_repo = customer_repo

    def get_all_customers(self):
        return self.customer_repo.get_all_customers()

    def get_customer_by_id(self, customer_id):
        return self.customer_repo.get_customer_by_id(customer_id)

    def create_customer(self, first_name, last_name, address):
        return self.customer_repo.create_customer(first_name, last_name, address)

    def update_customer(self, customer_id, new_first_name, new_last_name, new_address):
        return self.customer_repo.update_customer(customer_id, new_first_name, new_last_name, new_address)
