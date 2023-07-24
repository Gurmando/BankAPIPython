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
