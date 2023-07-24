class CustomerController:
    def __init__(self, customer_service):
        self.customer_service = customer_service

    def get_all_customers(self):
        all_customers = self.customer_service.get_all_customers()
        return all_customers

    def get_customer_by_id(self, customer_id):
        customer = self.customer_service.get_customer_by_id(customer_id)
        if customer:
            return {
                "id": customer.id,
                "first_name": customer.first_name,
                "last_name": customer.last_name,
                "address": customer.address
            }
        else:
            return None

    def create_customer(self, first_name, last_name, address):
        new_customer = self.customer_service.create_customer(first_name, last_name, address)
        return {
            "id": new_customer.id,
            "first_name": new_customer.first_name,
            "last_name": new_customer.last_name,
            "address": new_customer.address
        }

    def update_customer(self, customer_id, new_first_name, new_last_name, new_address):
        update_successful = self.customer_service.update_customer(
            customer_id, new_first_name, new_last_name, new_address
        )
        return update_successful
