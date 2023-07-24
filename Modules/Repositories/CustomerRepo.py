class CustomerRepo:
    def get_all_customers(self):
        customers = [
            {"id": 1, "first_name": "Darus", "last_name": "Slah", "address": "123 Main St"},
            {"id": 2, "first_name": "Gurmanjot", "last_name": "Singh", "address": "123 Main St"},
            {"id": 3, "first_name": "Amine", "last_name": "Mohammed", "address": "123 Main St"}
        ]
        return customers

    def get_customer_by_id(self, customer_id):
        customers = self.get_all_customers()
        for customer in customers:
            if customer["id"] == customer_id:
                return Customer(customer["id"], customer["first_name"], customer["last_name"], customer["address"])
        return None

    def create_customer(self, first_name, last_name, address):
        new_customer_id = len(self.get_all_customers()) + 1
        return Customer(new_customer_id, first_name, last_name, address)

    def update_customer(self, customer_id, new_first_name, new_last_name, new_address):
        customers = self.get_all_customers()
        for customer in customers:
            if customer["id"] == customer_id:
                customer["first_name"] = new_first_name
                customer["last_name"] = new_last_name
                customer["address"] = new_address
                return True  # Update successful
        return False  # Customer not found

    def get_customer_by_account(self, account_id):
        customers = get_all_customers()
        for customer in customers:
            if account_id in customer.get("accounts", []):
                return Customer(customer["id"], customer["first_name"], customer["last_name"], customer["address"])
        return None

