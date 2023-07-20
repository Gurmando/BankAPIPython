from flask import Flask, request, jsonify

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
