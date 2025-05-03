from flask import Blueprint, jsonify, request
from flask_cors import CORS, cross_origin
from auth.auth_middleware import verify_id
import requests
import csv
import os
from auth.auth_middleware import token_required

ALPHA_ADVANTAGE_KEY = os.environ.get("ALPHA_ADVANTAGE_KEY", None)
earnings = Blueprint('earnings', __name__, url_prefix='/api/v1')
search = Blueprint('search', __name__, url_prefix='/api/v1')
timeSeries = Blueprint('timeSeries', __name__, url_prefix='/api/v1')

@earnings.after_request
def after_request(response): 
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add("Access-Control-Allow-Methods", "DELETE, POST, GET, OPTIONS")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
    print(response)
    return response
    
@search.route('search/<searchTerm>', methods=['GET'])
def ticker_search(searchTerm):
    url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + searchTerm + "&apikey=" + ALPHA_ADVANTAGE_KEY
    r = requests.get(url)
    data = r.json()
    return data

@earnings.route('earnings_calendar', methods=['GET', 'OPTIONS'])
def earnings_calendar():
    print(request)
    url = "https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&horizon=3month&datatype=json&apikey=" + ALPHA_ADVANTAGE_KEY
    data = ''
    print(request.headers['Authorization'])
    with requests.Session() as s:
        download = s.get(url)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            data += '|'.join(row)
            data += '~'
    return data

@timeSeries.route('issuer/<symbol>/timeSeries/weekly', methods=['GET'])
def time_series_weekly(symbol):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=" + symbol + "&apikey=" + ALPHA_ADVANTAGE_KEY
    r = requests.get(url)
    data = r.json()
    return data
