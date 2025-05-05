from flask import Blueprint, jsonify
#from auth.auth_middleware import verify_id
import requests
import os
import json
import re

ALPHA_ADVANTAGE_KEY = os.environ.get("ALPHA_ADVANTAGE_KEY", None)

earnings = Blueprint('earnings', __name__, url_prefix='/api/v1')
search = Blueprint('search', __name__, url_prefix='/api/v1')
timeSeries = Blueprint('timeSeries', __name__, url_prefix='/api/v1')

@search.route('search/<searchTerm>', methods=['GET'])
def ticker_search(searchTerm):
    #url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=" + searchTerm + "&apikey=" + ALPHA_ADVANTAGE_KEY
    #r = requests.get(url)
    #data = r.json()
    #return data
    with open('data/search_results_ibm.json', 'r') as file:
        data = json.load(file)
        print(data['bestMatches'])
        cleaned_data = [
            {re.sub(r"^\d+\.\s*", "", k): v for k, v in match.items()}
            for match in data['bestMatches']
        ]
        return cleaned_data

@earnings.route('earnings_calendar', methods=['GET', 'OPTIONS'])
def earnings_calendar():
    with open('data/earnings_calendar.csv', 'r') as file:
        x = file.read()
        print(x)
        return jsonify(x)
       
@timeSeries.route('issuer/<symbol>/timeSeries/weekly', methods=['GET'])
def time_series_weekly(symbol):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=" + symbol + "&apikey=" + ALPHA_ADVANTAGE_KEY
    r = requests.get(url)    
    data = r.json()
    return data
