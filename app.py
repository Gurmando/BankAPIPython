from werkzeug.wrappers import Request, Response
from flask import Flask, jsonify

#working on learning import statements and modules
import Account
import Customer
import Address

app = Flask(__name__)

@app.route('/person/')
def hello():
    return jsonify({'name': 'Jimit',
                    'address': 'India'})

if __name__ == "__mainapi__":
    app.run(host='localhost', port=5000)

@app.route('/person/')
def hello():
    return jsonify({'name': 'Jimit',
                    'address': 'India'})

