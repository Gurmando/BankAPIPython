from flask import Flask, request, jsonify, session


from Modules.Repositories.BillRepo import BillRepo
from Modules.Services.BillService import BillService

app = Flask(__name__)

bill_repo = BillRepo()
bill_service = BillService(bill_repo)


@app.route('/bill', methods=['POST'])
def create_bill():
    data = request.get_json()
    bill = bill_service.create_bill(data['id'], data['payee'], data['bill_status'], data['nick_name'],
                                    data['paymentAmount'])
    return jsonify(bill.__dict__), 201


@app.route('/bill/<id>', methods=['GET'])
def get_bill(id):
    bill = bill_service.get_bill(id)
    return jsonify(bill.__dict__), 200


@app.route('/bill/<id>', methods=['DELETE'])
def delete_bill(id):
    bill_service.delete_bill(id)


@app.route('/bills/<id>', methods=['PUT'])
def update_bill(id):
    data = request.get_json()
    bill_repo = BillRepo(session) 
    bill_service = BillService(bill_repo)
    updated_bill = bill_service.update_bill(id, data.get('payee'), data.get('bill_status'), data.get('nick_name'),
                                            data.get('payment_amount'))
    if updated_bill:
        return jsonify(updated_bill.__dict__), 200

