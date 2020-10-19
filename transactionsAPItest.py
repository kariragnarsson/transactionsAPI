import requests

# checks if correct requests give 200 status code
def test_allTransactions_200():
     response = requests.get("http://localhost:5000/transactions/api/v1.0/allTransactions?date=2020-07-06&merchantId=9876503")
     assert response.status_code == 200
def test_netTotal_200():
     response = requests.get("http://localhost:5000/transactions/api/v1.0/netTotal?date=2020-07-02&merchantId=9876501")
     assert response.status_code == 200
def test_voidTransaction_200():
     response = requests.put("http://localhost:5000/transactions/api/v1.0/voidTransaction?merchantId=9876503&transactionId=cf75e899-05a3-4712-82a8-9d394d6973af")
     assert response.status_code == 200

# checks if correct requests output json
def test_allTransactions_JSON():
     response = requests.get("http://localhost:5000/transactions/api/v1.0/allTransactions?date=2020-07-06&merchantId=9876503")
     assert response.headers["Content-Type"] == "application/json"
def test_netTotal_JSON():
     response = requests.get("http://localhost:5000/transactions/api/v1.0/netTotal?date=2020-07-02&merchantId=9876501")
     assert response.headers["Content-Type"] == "application/json"
def test_voidTransaction_JSON():
     response = requests.put("http://localhost:5000/transactions/api/v1.0/voidTransaction?merchantId=9876503&transactionId=cf75e899-05a3-4712-82a8-9d394d6973af")
     assert response.headers["Content-Type"] == "application/json"

# check output of response