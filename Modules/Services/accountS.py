from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

# Function to establish a MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Lina2011",
        database="AmineAccountBank"
    )

class Account:
    def __init__(self, account_id, type, nickname, rewards, balance, customer):
        self.id = account_id
        self.type = type
        self.nickname = nickname
        self.rewards = rewards
        self.balance = balance
        self.customer = customer

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["type"],
            data["nickname"],
            data["rewards"],
            data["balance"],
            data["customer"]
        )


    # Route to get all accounts
    @staticmethod
    @app.route('/accounts', methods=['GET'])
    def get_all_accounts():
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts")
        accounts_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(accounts_data)

    # Route to get account details by account ID
    @staticmethod
    @app.route('/accounts/<int:account_id>', methods=['GET'])
    def get_account_by_id(account_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts WHERE id = %s", (account_id,))
        account_data = cursor.fetchone()
        cursor.close()
        conn.close()
        if account_data:
            account = Account.from_dict(account_data)
            return jsonify(account.__dict__)
        else:
            abort(404)

    # Route to get all accounts for a specific customer
    @staticmethod
    @app.route('/customers/<string:customer_id>/accounts', methods=['GET'])
    def get_accounts_for_customer(customer_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM accounts WHERE customer = %s", (customer_id,))
        customer_accounts_data = cursor.fetchall()
        cursor.close()
        conn.close()
        customer_accounts = [Account.from_dict(data) for data in customer_accounts_data]
        return jsonify([acc.__dict__ for acc in customer_accounts])

    # Route to create an account for a specific customer
    @staticmethod
    @app.route('/customers/<string:customer_id>/accounts', methods=['POST'])
    def create_account_for_customer(customer_id):
        data = request.get_json()
        account = Account(
            None,
            data.get("type"),
            data.get("nickname"),
            data.get("rewards"),
            data.get("balance"),
            customer_id
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO accounts (type, nickname, rewards, balance, customer) VALUES (%s, %s, %s, %s, %s)",
                       (account.type, account.nickname, account.rewards, account.balance, account.customer))
        conn.commit()
        account.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Account created successfully", "account": account.__dict__}), 201

    # Route to update an existing account
    @staticmethod
    @app.route('/accounts/<int:account_id>', methods=['PUT'])
    def update_account(account_id):
        data = request.get_json()
        account = Account(
            account_id,
            data.get("type"),
            data.get("nickname"),
            data.get("rewards"),
            data.get("balance"),
            None
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET type = %s, nickname = %s, rewards = %s, balance = %s WHERE id = %s",
                       (account.type, account.nickname, account.rewards, account.balance, account.id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Account updated successfully"}), 200

    # Route to delete an existing account
    @staticmethod
    @app.route('/accounts/<int:account_id>', methods=['DELETE'])
    def delete_account(account_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM accounts WHERE id = %s", (account_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Account deleted successfully"}), 200


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




bills_data = []


@app.route('/bills', methods=['GET'])
def get_all_bills():
    return jsonify(bills_data)


@app.route('/bills/<int:bill_id>', methods=['GET'])
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
