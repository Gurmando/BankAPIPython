from importlib.resources import Resource

from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_restful import reqparse
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

from Modules.Exceptions import ResourceNotFoundException

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


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"


class MediumType(Enum):
    CASH = "CASH"
    CHECK = "CHECK"


class StatusType(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class Deposit:
    def __init__(self, id, type, transaction_date, status, payee_id, medium, amount, description, account):
        self.id = id
        self.type = type
        self.transaction_date = transaction_date
        self.status = status
        self.payee_id = payee_id
        self.medium = medium
        self.amount = amount
        self.description = description
        self.account = account


# Utility function to convert Enums to strings
def enum_to_str(enum_val):
    return enum_val.value if enum_val else None


class DepositController(Resource):
    def get(self, deposit_id):
        if deposit_id in deposits:
            deposit = deposits[deposit_id]
            return deposit, 200
        else:
            return {"message": f"Deposit with ID #{deposit_id} not found"}, 404

    def post(self):
        data = request.get_json()
        # Perform validation on the data received in the request
        # For example, check if all required fields are present
        if not data.get('amount') or not data.get('description'):
            return {"message": "Amount and description are required fields"}, 400

        global next_deposit_id
        deposit_id = next_deposit_id
        next_deposit_id += 1

        new_deposit = {
            'id': deposit_id,
            'amount': data['amount'],
            'description': data['description']
            # Add other fields as needed
        }

        deposits[deposit_id] = new_deposit
        return new_deposit, 201

    def put(self, deposit_id):
        if deposit_id in deposits:
            data = request.get_json()
            # Perform validation on the data received in the request
            # For example, check if all required fields are present
            if not data.get('amount') or not data.get('description'):
                return {"message": "Amount and description are required fields"}, 400

            deposit = deposits[deposit_id]
            deposit['amount'] = data['amount']
            deposit['description'] = data['description']
            # Update other fields as needed

            deposits[deposit_id] = deposit
            return deposit, 200
        else:
            return {"message": f"Deposit with ID #{deposit_id} not found"}, 404

    def delete(self, deposit_id):
        if deposit_id in deposits:
            del deposits[deposit_id]
            return "", 204  # No content
        else:
            return {"message": f"Deposit with ID #{deposit_id} not found"}, 404


api.add_resource(DepositController, '/accounts/<int:accountId>/deposits', '/deposits/<int:depositId>')

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    app.run(host='localhost', port=5000)
