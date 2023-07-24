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
