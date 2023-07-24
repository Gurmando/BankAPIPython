
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

from flask_restful import Resource, reqparse
from Exceptions import ResourceNotFoundException
from Models.CustomerModel import Customer
from Services.CustomerService import CustomerService

parser = reqparse.RequestParser()
parser.add_argument('first_name', type=str, help='First name of the customer')
parser.add_argument('last_name', type=str, help='Last name of the customer')


class CustomerController(Resource):
    def __init__(self):
        self.service = CustomerService(CustomerRepository())

    def get(self):
        customers = self.service.get_all_customers()
        serialized_customers = [{'id': customer.id, 'first_name': customer.first_name, 'last_name': customer.last_name}
                                for customer in customers]

        return {'message': 'Successfully retrieved all customers', 'data': serialized_customers}, 200

    def post(self):
        args = parser.parse_args()
        customer = self.service.create_customer(args)

        return {'message': 'Customer created successfully',
                'data': {'id': customer.id, 'first_name': customer.first_name, 'last_name': customer.last_name}}, 201

    def put(self, customer_id):
        args = parser.parse_args()

        try:
            customer = self.service.update_customer(customer_id, args)
        except ResourceNotFoundException:
            return {'message': f'Customer with ID {customer_id} not found'}, 404

        return {'message': 'Customer updated successfully',
                'data': {'id': customer.id, 'first_name': customer.first_name, 'last_name': customer.last_name}}, 200

    def delete(self, customer_id):
        try:
            self.service.delete_customer(customer_id)
        except ResourceNotFoundException:
            return {'message': f'Customer with ID {customer_id} not found'}, 404

        return {'message': 'Customer deleted successfully'}, 204

