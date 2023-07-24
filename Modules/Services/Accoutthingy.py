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
