from flask import Flask, jsonify, request, abort
import mysql.connector

app = Flask(__name__)

# Sample account data (to simulate database)
customers_data = []

accounts_data = []

deposits_data = []

withdrawals_data = []

# Account types enum
account_types = ["Savings", "Checking", "Credit"]


# Function to establish a MySQL connection
def get_mysql_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="Gman1234!",
        database="pythonbank"
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


class Deposit:

    def __init__(self, deposit_id, type, transaction_date, status, payee_id, medium, amount, description, account):
        self.id = deposit_id
        self.type = type
        self.transaction_date = transaction_date
        self.status = status
        self.payee_id = payee_id
        self.medium = medium
        self.amount = amount
        self.description = description
        self.account = account

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["type"],
            data["transaction_date"],
            data["status"],
            data["payee_id"],
            data["medium"],
            data["amount"],
            data["description"],
            data["account"]
        )

    @staticmethod
    # Route to get all deposits
    @app.route('/deposits', methods=['GET'])
    def get_all_deposits():
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM deposits")
        deposits_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(deposits_data)

    @staticmethod
    # Route to get deposit details by deposit ID
    @app.route('/deposits/<int:deposit_id>', methods=['GET'])
    def get_deposit_by_id(deposit_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM deposits WHERE id = %s", (deposit_id,))
        deposit_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if deposit_data:
            deposit = Deposit.from_dict(deposit_data)
            return jsonify(deposit.__dict__)
        else:
            abort(404)

    @staticmethod
    # Route to get all deposits for a specific account
    @app.route('/accounts/<int:account_id>/deposits', methods=['GET'])
    def get_deposits_for_account(account_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM deposits WHERE account = %s", (account_id,))
        account_deposits_data = cursor.fetchall()
        cursor.close()
        conn.close()

        account_deposits = [Deposit.from_dict(data) for data in account_deposits_data]
        return jsonify([dep.__dict__ for dep in account_deposits])

    @staticmethod
    @app.route('/accounts/<int:account_id>/deposits', methods=['POST'])
    def create_deposit_for_account(account_id):
        data = request.get_json()
        deposit = Deposit(
            None,
            data.get("type"),
            data.get("transaction_date"),
            data.get("status"),
            data.get("payee_id"),
            data.get("medium"),
            data.get("amount"),
            data.get("description"),
            account_id
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO deposits (type, transaction_date, status, payee_id, medium, amount, description, account) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (deposit.type, deposit.transaction_date, deposit.status, deposit.payee_id, deposit.medium, deposit.amount,
             deposit.description, deposit.account))
        conn.commit()
        deposit.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Deposit created successfully", "deposit": deposit.__dict__}), 201

    @staticmethod
    # Route to update an existing deposit
    @app.route('/deposits/<int:deposit_id>', methods=['PUT'])
    def update_deposit(deposit_id):
        data = request.get_json()
        deposit = Deposit(
            deposit_id,
            data.get("type"),
            data.get("transaction_date"),
            data.get("status"),
            data.get("payee_id"),
            data.get("medium"),
            data.get("amount"),
            data.get("description"),
            None
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE deposits SET type = %s, transaction_date = %s, status = %s, payee_id = %s, medium = %s, "
                       "amount = %s, description = %s WHERE id = %s",
                       (deposit.type, deposit.transaction_date, deposit.status, deposit.payee_id, deposit.medium,
                        deposit.amount, deposit.description, deposit.id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Deposit updated successfully"}), 200

    @staticmethod
    # Route to delete an existing deposit
    @app.route('/deposits/<int:deposit_id>', methods=['DELETE'])
    def delete_deposit(deposit_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM deposits WHERE id = %s", (deposit_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Deposit deleted successfully"}), 200


class Withdrawal:

    def __init__(self, withdrawal_id, type, transaction_date, status, payee_id, medium, amount, description, account):
        self.id = withdrawal_id
        self.type = type
        self.transaction_date = transaction_date
        self.status = status
        self.payee_id = payee_id
        self.medium = medium
        self.amount = amount
        self.description = description
        self.account = account

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id"],
            data["type"],
            data["transaction_date"],
            data["status"],
            data["payee_id"],
            data["medium"],
            data["amount"],
            data["description"],
            data["account"]
        )
    @staticmethod
    # Route to get all withdrawals
    @app.route('/withdrawals', methods=['GET'])
    def get_all_withdrawals():
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM withdrawals")
        withdrawals_data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(withdrawals_data)

    @staticmethod
    # Route to get withdrawal details by withdrawal ID
    @app.route('/withdrawals/<int:withdrawal_id>', methods=['GET'])
    def get_withdrawal_by_id(withdrawal_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM withdrawals WHERE id = %s", (withdrawal_id,))
        withdrawal_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if withdrawal_data:
            withdrawal = Deposit.from_dict(withdrawal_data)
            return jsonify(withdrawal.__dict__)
        else:
            abort(404)

    @staticmethod
    # Route to get all withdrawals for a specific account
    @app.route('/accounts/<int:account_id>/withdrawals', methods=['GET'])
    def get_withdrawals_for_account(account_id):
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM withdrawals WHERE account = %s", (account_id,))
        account_withdrawals_data = cursor.fetchall()
        cursor.close()
        conn.close()

        account_withdrawals = [Deposit.from_dict(data) for data in account_withdrawals_data]
        return jsonify([withdrawal.__dict__ for withdrawal in account_withdrawals])

    @staticmethod
    @app.route('/accounts/<int:account_id>/withdrawals', methods=['POST'])
    def create_withdrawal_for_account(account_id):
        data = request.get_json()
        withdrawal = Withdrawal(
            None,
            data.get("type"),
            data.get("transaction_date"),
            data.get("status"),
            data.get("payee_id"),
            data.get("medium"),
            data.get("amount"),
            data.get("description"),
            account_id
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO withdrawals (type, transaction_date, status, payee_id, medium, amount, description, account) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (withdrawal.type, withdrawal.transaction_date, withdrawal.status, withdrawal.payee_id, withdrawal.medium,
             withdrawal.amount, withdrawal.description, withdrawal.account))
        conn.commit()
        withdrawal.id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({"message": "Withdrawal created successfully", "withdrawal": withdrawal.__dict__}), 201

    @staticmethod
    # Route to update an existing withdrawal
    @app.route('/withdrawals/<int:withdrawal_id>', methods=['PUT'])
    def update_withdrawal(withdrawal_id):
        data = request.get_json()
        withdrawal = Deposit(
            withdrawal_id,
            data.get("type"),
            data.get("transaction_date"),
            data.get("status"),
            data.get("payee_id"),
            data.get("medium"),
            data.get("amount"),
            data.get("description"),
            None
        )
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE withdrawals SET type = %s, transaction_date = %s, status = %s, payee_id = %s, medium = %s, "
            "amount = %s, description = %s WHERE id = %s",
            (withdrawal.type, withdrawal.transaction_date, withdrawal.status, withdrawal.payee_id, withdrawal.medium,
             withdrawal.amount, withdrawal.description, withdrawal.id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Withdrawal updated successfully"}), 200

    @staticmethod
    # Route to delete an existing withdrawal
    @app.route('/withdrawals/<int:withdrawal_id>', methods=['DELETE'])
    def delete_withdrawal(withdrawal_id):
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM withdrawals WHERE id = %s", (withdrawal_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Withdrawal deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
