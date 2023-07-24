from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

host = 'your_database_host'
user = 'your_database_username'
password = 'your_database_password'
database = 'your_database_name'

# Create a connection to the database
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)

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

deposits_data = []

withdrawals_data = []

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


# Route to get all deposits
@app.route('/deposits', methods=['GET'])
def get_all_deposits():
    return jsonify(deposits_data)


# Route to get deposit details by deposit ID
@app.route('/deposits/<int:deposit_id>', methods=['GET'])
def get_deposit_by_id(deposit_id):
    deposit = next((dep for dep in deposits_data if dep["id"] == deposit_id), None)
    if deposit:
        return jsonify(deposit)
    else:
        abort(404)


# Route to get all deposits for a specific account
@app.route('/accounts/<int:account_id>/deposits', methods=['GET'])
def get_deposits_for_account(account_id):
    account_deposits = [dep for dep in deposits_data if dep["account"] == account_id]
    return jsonify(account_deposits)


# Route to create a deposit for a specific account
@app.route('/accounts/<int:account_id>/deposits', methods=['POST'])
def create_deposit_for_account(account_id):
    data = request.get_json()
    deposit = {
        "id": len(deposits_data) + 1,
        "type": data.get("type"),
        "transaction_date": data.get("transaction_date"),
        "status": data.get("status"),
        "payee_id": data.get("payee_id"),
        "medium": data.get("medium"),
        "amount": data.get("amount"),
        "description": data.get("description"),
        "account": account_id
    }
    deposits_data.append(deposit)
    return jsonify({"message": "Deposit created successfully"}), 201


# Route to update an existing deposit
@app.route('/deposits/<int:deposit_id>', methods=['PUT'])
def update_deposit(deposit_id):
    data = request.get_json()
    deposit = next((dep for dep in deposits_data if dep["id"] == deposit_id), None)
    if deposit:
        deposit.update({
            "id": len(accounts_data) + 1,
            "type": data.get("type"),
            "transaction_date": data.get("transaction_date"),
            "status": data.get("status"),
            "payee_id": data.get("payee_id"),
            "medium": data.get("medium"),
            "amount": data.get("amount"),
            "description": data.get("description"),
        })
        return jsonify({"message": "Deposit updated successfully"})
    else:
        abort(404)


# Route to delete an existing deposit
@app.route('/deposits/<int:deposit_id>', methods=['DELETE'])
def delete_deposit(deposit_id):
    global deposits_data
    deposits_data = [dep for dep in deposits_data if dep["id"] != deposit_id]
    return jsonify({"message": "Deposit deleted successfully"})


# Route to get all withdrawals
@app.route('/withdrawals', methods=['GET'])
def get_all_withdrawals():
    return jsonify(withdrawals_data)


# Route to get withdrawal details by withdrawal ID
@app.route('/withdrawals/<int:withdrawal_id>', methods=['GET'])
def get_withdrawal_by_id(withdrawal_id):
    withdrawal = next((w for w in withdrawals_data if w["id"] == withdrawal_id), None)
    if withdrawal:
        return jsonify(withdrawal)
    else:
        abort(404)


# Route to get all withdrawals for a specific account
@app.route('/accounts/<int:account_id>/withdrawals', methods=['GET'])
def get_withdrawals_for_account(account_id):
    account_withdrawals = [w for w in withdrawals_data if w["account"] == account_id]
    return jsonify(account_withdrawals)


# Route to create a withdrawal for a specific account
@app.route('/accounts/<int:account_id>/withdrawals', methods=['POST'])
def create_withdrawal_for_account(account_id):
    data = request.get_json()
    withdrawal = {
        "type": "Withdrawal",
        "transaction_date": data.get("transaction_date"),
        "status": "Completed",
        "payee_id": data.get("payee_id"),
        "medium": data.get("medium"),
        "amount": data.get("amount"),
        "description": data.get("description"),
        "account": account_id
    }
    withdrawals_data.append(withdrawal)
    return jsonify({"message": "Withdrawal created successfully"}), 201


# Route to update an existing withdrawal
@app.route('/withdrawals/<int:withdrawal_id>', methods=['PUT'])
def update_withdrawal(withdrawal_id):
    data = request.get_json()
    withdrawal = next((w for w in withdrawals_data if w["id"] == withdrawal_id), None)
    if withdrawal:
        withdrawal.update({
            "transaction_date": data.get("transaction_date"),
            "payee_id": data.get("payee_id"),
            "medium": data.get("medium"),
            "amount": data.get("amount"),
            "description": data.get("description"),
        })
        return jsonify({"message": "Withdrawal updated successfully"})
    else:
        abort(404)


# Route to delete an existing withdrawal
@app.route('/withdrawals/<int:withdrawal_id>', methods=['DELETE'])
def delete_withdrawal(withdrawal_id):
    global withdrawals_data
    withdrawals_data = [w for w in withdrawals_data if w["id"] != withdrawal_id]
    return jsonify({"message": "Withdrawal deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
