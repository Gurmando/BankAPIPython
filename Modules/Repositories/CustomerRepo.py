
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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Models.CustomerModel import Customer


class CustomerRepository:
    def __init__(self):
        self.engine = create_engine('mysql+mysqlconnector://your_username:your_password@localhost/your_database')
        self.Session = sessionmaker(bind=self.engine)

    def create_customer(self, customer_data):
        session = self.Session()
        customer = Customer(
            first_name=customer_data['first_name'],
            last_name=customer_data['last_name']
        )
        session.add(customer)
        session.commit()
        session.close()
        return customer

    def get_customer_by_id(self, customer_id):
        session = self.Session()
        customer = session.query(Customer).get(customer_id)
        session.close()
        return customer

    def get_all_customers(self):
        session = self.Session()
        customers = session.query(Customer).all()
        session.close()
        return customers

    def update_customer(self, customer_id, customer_data):
        session = self.Session()
        customer = session.query(Customer).get(customer_id)
        if customer:
            customer.first_name = customer_data.get('first_name', customer.first_name)
            customer.last_name = customer_data.get('last_name', customer.last_name)
            session.commit()
        session.close()
        return customer

    def delete_customer(self, customer_id):
        session = self.Session()
        customer = session.query(Customer).get(customer_id)
        if customer:
            session.delete(customer)
            session.commit()
        session.close()
        return customer

