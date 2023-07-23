#
# from flask import Flask, jsonify, request
# from flask_mysqldb import MySQL
# from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base
#
# app = Flask(__name__)
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_PORT'] = 3306
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Gman1234!'
# app.config['MYSQL_DB'] = 'PythonBank'
#
# mysql = MySQL(app)
#
# engine = create_engine('mysql+pymysql://root:Gman1234!@localhost/pythonbank?charset=utf8mb4', echo=True)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
#
#
# class Customer(Base):
#     __tablename__ = 'customers'
#
#     id = Column(Integer, primary_key=True)
#     first_name = Column(String(25), nullable=False)
#     last_name = Column(String(25), nullable=False)
#     address = Column(String(100), nullable=False)
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'first_name': self.first_name,
#             'last_name': self.last_name,
#             'address': self.address
#         }
#
#
# class Account(Base):
#     __tablename__ = 'accounts'
#
#     id = Column(Integer, primary_key=True)
#     type = Column(String(50), nullable=False)
#     nickname = Column(String(50), nullable=False)
#     rewards = Column(Integer)
#     balance = Column(Float, nullable=False)
#     customer_id = Column(Integer, ForeignKey('customers.id'))
#     customer = relationship('Customer', backref='accounts')
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#              'account_type': self.account_type,
#             'nickname': self.nickname,
#             'rewards': self.rewards,
#             'balance': self.balance
#         }
#
#
# class Deposit(Base):
#     __tablename__ = 'deposits'
#
#     id = Column(Integer, primary_key=True)
#     type = Column(String(50))
#     transaction_date = Column(String(50))
#     status = Column(String(50))
#     payee_id = Column(Integer)
#     medium = Column(String(50), nullable=False)
#     amount = Column(Float)
#     description = Column(String(50))
#     account_id = Column(Integer, ForeignKey('accounts.id'))
#     account = relationship('Account', backref='deposits')
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'type': self.type,
#             'transaction_date': self.transaction_date,
#             'status': self.status,
#             'payee_id': self.payee_id,
#             'medium': self.medium,
#             'amount': self.amount,
#             'description': self.description,
#             'account_id': self.account_id
#         }
#
#
# class Withdrawal(Base):
#     __tablename__ = 'withdrawal'
#
#     id = Column(Integer, primary_key=True)
#     type = Column(String(50))
#     transaction_date = Column(String(50))
#     status = Column(String(50))
#     payee_id = Column(Integer)
#     medium = Column(String(50), nullable=False)
#     amount = Column(Float)
#     description = Column(String(50))
#     account_id = Column(Integer, ForeignKey('accounts.id'))
#     account = relationship('Account', backref='deposits')
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'type': self.type,
#             'transaction_date': self.transaction_date,
#             'status': self.status,
#             'payee_id': self.payee_id,
#             'medium': self.medium,
#             'amount': self.amount,
#             'description': self.description,
#             'account_id': self.account_id
#         }
#
#
# @app.route('/customers/')
# def get_customers():
#     session = Session()
#     customers = session.query(Customer).all()
#     customer_dicts = [customer.to_dict() for customer in customers]
#     session.close()
#     return jsonify(customer_dicts)
#
#
# @app.route('/accounts/')
# def get_accounts():
#     session = Session()
#     accounts = session.query(Account).all()
#     account_dicts = [account.to_dict() for account in accounts]
#     session.close()
#     return jsonify(account_dicts)
#
#
# @app.route('/customer', methods=['POST'])
# def add_customers():
#     customer = Customer(**request.get_json())
#     session = Session()
#     session.add(customer)
#     session.commit()
#     session.close()
#     return '', 204
#
#
# if __name__ == "__main__":
#     Base.metadata.create_all(engine)
#     app.run(host='localhost', port=5000)
#
