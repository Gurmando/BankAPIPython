from flask import Flask, jsonify, request, abort
import mysql.connector

from Modules.POJOs.Bill import Bill

app = Flask(__name__)


# Function to establish a MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="DarusJSlah98",
        database="PythonBankAPI"
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

    class Bill:
        def __init__(self, bill_id, type, status, payee, nickname, creation_date, payment_date, recurring_date,
                     upcoming_payment_date, payment_amount):
            self.id = bill_id
            self.type = type
            self.status = status
            self.payee = payee
            self.nickname = nickname
            self.creation_date = creation_date
            self.payment_date = payment_date
            self.recurring_date = recurring_date
            self.upcoming_payment_date = upcoming_payment_date
            self.payment_amount = payment_amount

        @classmethod
        def from_dict(cls, data):
            return cls(
                data["id"],
                data["type"],
                data["status"],
                data["payee"],
                data["nickname"],
                data["creation_date"],
                data["payment_date"],
                data["recurring_date"],
                data["upcoming_payment_date"],
                data["payment_amount"]
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


bills_data = []


@app.route('/bills', methods=['GET'])
def get_all_bills():
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bills")
    bills_data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(bills_data)


@app.route('/bills/<int:bill_id>', methods=['GET'])
def get_bill_by_id(bill_id):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bill WHERE id = %s", (bill_id,))
    bill_data = cursor.fetchone()
    cursor.close()
    conn.close()
    bill = next((b for b in bills_data if b["id"] == bill_id), None)
    if bill_data:
        bill = Bill.from_dict(bill_data)
        return jsonify(bill.__dict__)
    else:
        abort(404)


@app.route('/accounts/<int:account_id>/bills', methods=['GET'])
def get_bills_for_account(account_id):
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bills WHERE account = %s", (account_id,))
    account_bills = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(account_bills)


@app.route('/accounts/<int:account_id>/bills', methods=['POST'])
def create_bill_for_account(account_id):
    data = request.get_json()

    # Create a new bill using the data from the request body
    bill = {
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

    conn = get_mysql_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO bills (type, status, payee, nickname, creation_date, payment_date, recurring_date, upcoming_payment_date, payment_amount, account) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (bill['type'], bill['status'], bill['payee'], bill['nickname'], bill['creation_date'], bill['payment_date'],
         bill['recurring_date'], bill['upcoming_payment_date'], bill['payment_amount'], bill['account'])
    )
    conn.commit()

    bill['id'] = cursor.lastrowid

    cursor.close()
    conn.close()

    return jsonify(bill), 201


@app.route('/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    data = request.get_json()
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM bills WHERE id = %s", (bill_id,))
    bill = cursor.fetchone()

    if bill:
        bill.update({
            "status": data.get("status"),
            "payee": data.get("payee"),
            "payment_amount": data.get("payment_amount")
        })
        cursor.execute(
            "UPDATE bills SET status = %s, payee = %s, payment_amount = %s WHERE id = %s",
            (bill['status'], bill['payee'], bill['payment_amount'], bill_id)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Bill updated successfully"})
    else:
        cursor.close()
        conn.close()
        abort(404)


@app.route('/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bills WHERE id = %s", (bill_id,))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Bill deleted successfully"})


if __name__ == '__main__':
    app.run(debug=True)
