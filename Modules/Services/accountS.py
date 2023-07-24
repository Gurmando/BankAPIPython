from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Sample account data (to simulate database)
accounts_data = [
    {
        "id": 1,
        "type": "Savings",
        "nickname": "Leon's savings account",
        "rewards": 100,
        "balance": 1000.0,
        "customer": "customer1"
    },
    {
        "id": 2,
        "type": "Checking",
        "nickname": "John's checking account",
        "rewards": 50,
        "balance": 5000.0,
        "customer": "customer2"
    }
]

# Account types enum
account_types = ["Savings", "Checking", "Credit"]


# Route to get all accounts
@app.route('/accounts', methods=['GET'])
def get_all_accounts():
    return jsonify(accounts_data)


# Route to get account details by account ID
@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account_by_id(account_id):
    account = next((acc for acc in accounts_data if acc["id"] == account_id), None)
    if account:
        return jsonify(account)
    else:
        abort(404)


# Route to get all accounts for a specific customer
@app.route('/customers/<string:customer_id>/accounts', methods=['GET'])
def get_accounts_for_customer(customer_id):
    customer_accounts = [acc for acc in accounts_data if acc["customer"] == customer_id]
    return jsonify(customer_accounts)


# Route to create an account for a specific customer
@app.route('/customers/<string:customer_id>/accounts', methods=['POST'])
def create_account_for_customer(customer_id):
    data = request.get_json()
    account = {
        "id": len(accounts_data) + 1,
        "type": data.get("type"),
        "nickname": data.get("nickname"),
        "rewards": data.get("rewards"),
        "balance": data.get("balance"),
        "customer": customer_id
    }
    accounts_data.append(account)
    return jsonify({"message": "Account created successfully"}), 201


# Route to update an existing account
@app.route('/accounts/<int:account_id>', methods=['PUT'])
def update_account(account_id):
    data = request.get_json()
    account = next((acc for acc in accounts_data if acc["id"] == account_id), None)
    if account:
        account.update({
            "type": data.get("type"),
            "nickname": data.get("nickname"),
            "rewards": data.get("rewards"),
            "balance": data.get("balance"),
        })
        return jsonify({"message": "Account updated successfully"})
    else:
        abort(404)


# Route to delete an existing account
@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):

    global accounts_data
    accounts_data = [acc for acc in accounts_data if acc["id"] != account_id]
    return jsonify({"message": "Account deleted successfully"})


bills_data = []


@app.route('/bills', methods=['GET'])
def get_all_bills():
    return jsonify(bills_data)


@app.route('/billsmer/<int:bill_id>', methods=['GET'])
def get_bill_by_id(bill_id):
    bill = next((b for b in bills_data if b["id"] == bill_id), None)
    if bill:
        return jsonify(bill)
    else:
        abort(404)


@app.route('/accounts/<int:account_id>/bills', methods=['GET'])
def get_bills_for_account(account_id):
    account_bills = [b for b in bills_data if b["account"] == account_id]
    return jsonify(account_bills)


@app.route('/accounts/<int:account_id>/bills', methods=['POST'])
def create_bill_for_account(account_id):
    data = request.get_json()

    # Create a new bill using the data from the request body
    bill = {
        "id": len(bills_data) + 1,
        "type": "Bill",
        "status": data.get("status"),
        "payee": data.get("payee"),
        "nickname": data.get("nickname"),
        "creation_date": data.get("creation_date"),
        "payment_date": data.get("payment_date"),
        "recurring_date": data.get("recurring_date"),
        "upcoming_payment_date": data.get("upcoming_payment_date"),
        "payment_amount": data.get("payment_amount"),
        "account": account_id
    }

    bills_data.append(bill)
    return jsonify(bill), 201


@app.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    data = request.get_json()
    bill = next((b for b in bills_data if b["id"] == bill_id), None)
    if bill:
        bill.update({
            "status": data.get("status"),
            "payee": data.get("payee"),
            "payment_amount": data.get("payment_amount")
        })
        return jsonify({"message": "Bill updated successfully"})
    else:
        abort(404)


@app.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    global bills_data
    bills_data = [b for b in bills_data if b["id"] != bill_id]
    return jsonify({"message": "Bill deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
