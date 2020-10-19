#!flask/bin/python
from flask import Flask, jsonify
from flask import make_response
from flask import request

from databaseCommunications import *

app = Flask(__name__)


# returns a description on the available API services
@app.route('/transactions/api/v1.0/', methods=['GET'])
def aboutApi():
    fileObject = open("about.txt","r")
    return fileObject.read()

# gets input from url parameters 'date' and merchandInput
# returns JSON response with all transactions for given date
@app.route('/transactions/api/v1.0/allTransactions', methods=['GET'])
def getTransactions():
    dateInput = request.args.get("date")
    merchantInput = request.args.get("merchantId")
    transactions = getAllTransactionsForDay(merchantInput,dateInput)
    return transactions

# gets net total of non-void transactions for given date and given merchant
# returns JSON object with sum and currency
@app.route('/transactions/api/v1.0/netTotal', methods=['GET'])
def getNet():
    dateInput = request.args.get("date")
    merchantInput = request.args.get("merchantId")
    total = getNetForDay(merchantInput,dateInput)
    return total

# voids a transaction given transaction id and merchant id
# sends back success or failure message
@app.route('/transactions/api/v1.0/voidTransaction', methods=['PUT'])
def voidTrans():
    merchantInput = request.args.get("merchantId")
    transactionInput = request.args.get("transactionId")
    transactionResult = voidTransaction(merchantInput,transactionInput)
    if transactionResult == "0":
        feedbackMessage =  {'feedback': "Update for transaction: " + transactionInput + " was not successful. Please check input",'success':False}
    else:
        feedbackMessage =  {'feedback': "Update for transaction: " + transactionInput + " was successful!",'success': True}

    return jsonify(feedbackMessage)

# gives error response
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found, please go to /transactions/api/v1.0 to see available functions'}), 404)

if __name__ == '__main__':
    app.run(debug=True)

    