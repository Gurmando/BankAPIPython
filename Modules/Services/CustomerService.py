
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

    def create_customer(self, customer_data):
        return self.customer_repo.create_customer(customer_data)

    def get_customer_by_id(self, customer_id):
        customer = self.customer_repo.find_by_id(customer_id)
        if not customer:
            raise ResourceNotFoundException("A customer with ID #" + str(customer_id) + " does not exist!")
        return customer

    def get_all_customers(self):
        return self.customer_repo.find_all_customers()

    def update_customer(self, customer_id, customer_data):
        customer = self.customer_repo.find_by_id(customer_id)
        if not customer:
            raise ResourceNotFoundException("A customer with ID #" + str(customer_id) + " does not exist!")

        if 'first_name' in customer_data:
            customer.first_name = customer_data['first_name']

        if 'last_name' in customer_data:
            customer.last_name = customer_data['last_name']

        return self.customer_repo.save(customer)

    def delete_customer(self, customer_id):
        customer = self.customer_repo.find_by_id(customer_id)
        if not customer:
            raise ResourceNotFoundException("A customer with ID #" + str(customer_id) + " does not exist!")
        return self.customer_repo.delete_by_id(customer_id)

