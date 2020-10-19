from flask import jsonify
import json
import psycopg2
from decimal import *


print(json.__version__)

# information for connection to database
connectionInfo = "dbname=test user=borgun password=salt"

# used to get all transactions for given day and merchant
# input: merchantId(str, length = 7), date(YYYY-MM-DD)
# output: JSON object containing all transactions for given day
def getAllTransactionsForDay(merchantId,date):
    conn = None
    results = None
    try:
        conn = psycopg2.connect(connectionInfo)
        cur = conn.cursor()

        cur.execute('SELECT array_to_json(array_agg(transactions))' +
        "FROM transactions WHERE transdate::date ='" + 
        date + "' AND merchant='" + merchantId + "'GROUP BY transdate ORDER BY transdate")
        sites_result = cur.fetchall()
        results = sites_result
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()    
    return jsonify(results)

# used to get net amount for given merchant for given day
# input merchantId(str, length = 7), date(YYYY-MM-DD)
# output: JSON object containing net amount and currency
def getNetForDay(merchantId,date):
    conn = None
    results = []
    try:
        conn = psycopg2.connect(connectionInfo)
        cur = conn.cursor()
        cur.execute('SELECT SUM("amount"),"currency"' +
        "FROM transactions WHERE transdate::date ='" + 
        date + "' AND merchant='" + merchantId + "' AND voided IS FALSE GROUP BY currency")
        sites_result = cur.fetchone()
        results = json.dumps(sites_result,default = fixOutput)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()    
    return jsonify(results)


# voids a transaction in the database given a certain unique id and merchant id
# input: merchantId(str, length = 7), transactionId(str,length = 36)
# output: "1" for successful update of item, "0" for failed attempt
def voidTransaction(merchantId,transactionId):
    conn = None
    updated = "0"
    try:
        conn = psycopg2.connect(connectionInfo)
        cur = conn.cursor()
        cur.execute('UPDATE transactions ' +
        'SET voided = true ' + 
        "WHERE id::text='" + transactionId + "' AND merchant='" + merchantId + "'")
        print(cur.rowcount)
        updated = cur.rowcount.__str__()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()    
    return updated


# usage: fixes output for json conversion
def fixOutput(o):
    if isinstance(o, Decimal):
        print(type(o))
        return float(o)
 