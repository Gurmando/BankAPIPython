class Customer:
    def __init__(self, id, first_name, last_name, address):
        self.id = int(id)
        self.first_name = str(first_name)
        self.last_name = str(last_name)
        self.address = address


def get_all_customers():
    # Assuming you have a database or data source where customers are stored
    # and you have a way to retrieve them, such as using an ORM or SQL queries
    # You can replace the comments with the appropriate code for your specific setup

    # Example code using a hypothetical database ORM
    # customers = CustomerModel.query.all()

    # Example code using SQL query
    # sql = "SELECT * FROM customers"
    # customers = execute_sql_query(sql)

    # Assuming customers is a list of customer objects or dictionaries
    customers = [
        {"id": 1, "first_name": "John", "last_name": "Doe", "address": "123 Main St"},
        {"id": 2, "first_name": "Jane", "last_name": "Smith", "address": "456 Elm St"},
        {"id": 3, "first_name": "Bob", "last_name": "Johnson", "address": "789 Oak St"}
    ]

    return customers


def get_customer_by_id(customer_id):
    customers = get_all_customers()
    for customer in customers:
        if customer["id"] == customer_id:
            return Customer(customer["id"], customer["first_name"], customer["last_name"], customer["address"])
    return None


def create_customer(first_name, last_name, address):
    # Assuming you have a database or data source where customers are stored
    # and you have a way to create a new customer, such as using an ORM or SQL queries
    # You can replace the comments with the appropriate code for your specific setup

    # Example code using a hypothetical database ORM
    # new_customer = CustomerModel(first_name=first_name, last_name=last_name, address=address)
    # db.session.add(new_customer)
    # db.session.commit()

    # Assuming you get an auto-generated ID from the database
    new_customer_id = 4

    return Customer(new_customer_id, first_name, last_name, address)


def update_customer(customer_id, new_first_name, new_last_name, new_address):
    # Assuming you have a database or data source where customers are stored
    # and you have a way to update an existing customer, such as using an ORM or SQL queries
    # You can replace the comments with the appropriate code for your specific setup

    # Example code using a hypothetical database ORM
    # customer = CustomerModel.query.get(customer_id)
    # if customer is not None:
    #     customer.first_name = new_first_name
    #     customer.last_name = new_last_name
    #     customer.address = new_address
    #     db.session.commit()

    # Placeholder update: assuming customers are stored in a list
    customers = get_all_customers()
    for customer in customers:
        if customer["id"] == customer_id:
            customer["first_name"] = new_first_name
            customer["last_name"] = new_last_name
            customer["address"] = new_address
            return True  # Update successful
    return False  # Customer not found


# Usage examples

# Get all customers
all_customers = get_all_customers()
for customer in all_customers:
    print(f"Customer: {customer['first_name']} {customer['last_name']}")

# Get customer by ID
customer_id = 2
customer = get_customer_by_id(customer_id)
if customer is not None:
    print(f"Customer: {customer.first_name} {customer.last_name}")
else:
    print("Customer not found.")

# Create a customer
new_customer = create_customer("Alice", "Johnson", "789 Pine St")
print(f"New customer created with ID: {new_customer.id}")

# Update an existing customer
existing_customer_id = 1
update_successful = update_customer(existing_customer_id, "John", "Smith", "123 Main St")
if update_successful:
    print("Customer updated successfully.")
else:
    print("Customer not found.")
