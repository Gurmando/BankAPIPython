
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

if __name__ == '__main__':
    app.run(debug=True)
=======
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Gman1234!'
app.config['MYSQL_DB'] = 'PythonBank'

mysql = MySQL(app)

engine = create_engine('mysql+pymysql://root:Gman1234!@localhost/pythonbank?charset=utf8mb4', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(25), nullable=False)
    last_name = Column(String(25), nullable=False)
    address = Column(String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address
        }


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    type = Column(String(50), nullable=False)
    nickname = Column(String(50), nullable=False)
    rewards = Column(Integer)
    balance = Column(Float, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    customer = relationship('Customer', backref='accounts')

    def to_dict(self):
        return {
            'id': self.id,
             'account_type': self.account_type,
            'nickname': self.nickname,
            'rewards': self.rewards,
            'balance': self.balance
        }


class Deposit(Base):
    __tablename__ = 'deposits'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    transaction_date = Column(String(50))
    status = Column(String(50))
    payee_id = Column(Integer)
    medium = Column(String(50), nullable=False)
    amount = Column(Float)
    description = Column(String(50))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', backref='deposits')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'transaction_date': self.transaction_date,
            'status': self.status,
            'payee_id': self.payee_id,
            'medium': self.medium,
            'amount': self.amount,
            'description': self.description,
            'account_id': self.account_id
        }


class Withdrawal(Base):
    __tablename__ = 'withdrawal'

    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    transaction_date = Column(String(50))
    status = Column(String(50))
    payee_id = Column(Integer)
    medium = Column(String(50), nullable=False)
    amount = Column(Float)
    description = Column(String(50))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    account = relationship('Account', backref='deposits')

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'transaction_date': self.transaction_date,
            'status': self.status,
            'payee_id': self.payee_id,
            'medium': self.medium,
            'amount': self.amount,
            'description': self.description,
            'account_id': self.account_id
        }


@app.route('/customers/')
def get_customers():
    session = Session()
    customers = session.query(Customer).all()
    customer_dicts = [customer.to_dict() for customer in customers]
    session.close()
    return jsonify(customer_dicts)


@app.route('/accounts/')
def get_accounts():
    session = Session()
    accounts = session.query(Account).all()
    account_dicts = [account.to_dict() for account in accounts]
    session.close()
    return jsonify(account_dicts)


@app.route('/customer', methods=['POST'])
def add_customers():
    customer = Customer(**request.get_json())
    session = Session()
    session.add(customer)
    session.commit()
    session.close()
    return '', 204


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='localhost', port=5000)
>>>>>>> origin/master
