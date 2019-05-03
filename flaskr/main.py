from flask import Blueprint, jsonify, abort, make_response, g
from flask import current_app, request, render_template, redirect, url_for
import sqlite3, requests, json, datetime
from .neuralNet import nn
import numpy as np


bp = Blueprint('main',__name__)

tickers=['GOOG','AMZN','NFLX','FB','AAPL','TSLA','HD','DIS','KR','ATVI']
dataset ={'GOOG':[],'AMZN':[],'NFLX':[],'FB':[],'AAPL':[],'TSLA':[],'HD':[],'DIS':[],'KR':[],'ATVI':[]}
def retrieve(data):
    this_data = data
    for i in range(len(data)):
        for each in data[i]['quotes']:
            dataset[tickers[i]].append(each)

@bp.route('/StockApp/')
def home():
    tickers = get_all_tickers()
    return render_template('main.html', company_tickers=tickers)


@bp.route('/StockApp/fetchStockPrice', methods=['GET'])
def priceFetchAPI():
    company_tickers = get_all_tickers()
    now = datetime.datetime.now()
    tickers = request.args.get('tickers')
    if tickers is not None:
        tickers = tickers.split("-")

    queryType = request.args.get('queryType')
    if queryType is None:
        queryType = "history"
    
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')

    data = dict_historical_data(tickers, queryType, startDate, endDate)
    retrieve(data)

    return render_template('table.html', data=data, company_tickers=company_tickers, queryType= queryType)




    
@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
    
@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    
# if __name__ == '__main__':
#     app.run(debug=True)
    
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def get_all_tickers():
    conn = None
    try:
        conn = get_db()
        command = "SELECT ticker FROM companies"
        cur = conn.cursor()
        companies = []

        for row in cur.execute(command):
            companies.append(row[0])

        cur.close()
        return companies



    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.commit()

    return companies


# Function receives a ticker as input and returns the historical data from the database as json
def dict_historical_data(tickers, queryType, startDate, endDate):
    ticker_data = []
    conn = None
    if queryType is None:
        queryType = "history"
    try:

        conn = get_db()
        for ticker in tickers:
            command = ""
            if queryType == "history":
                    command = "SELECT * FROM quotes WHERE ticker = ? "
                    
            elif queryType == "average":
                    command = "SELECT ticker, date-time, AVG(open), AVG(high), AVG(low), AVG(close), AVG(volume) FROM quotes WHERE ticker = ? "
                    
            elif queryType == "low":
                    command = "SELECT ticker, date-time, MIN(open), MIN(high), MIN(low), MIN(close), MIN(volume) FROM quotes WHERE ticker = ? "
                    
            elif queryType == "high":
                    command = "SELECT ticker, date-time, MAX(open), MAX(high), MAX(low), MAX(close), MAX(volume) FROM quotes WHERE ticker = ? "
                    
            
            dateCommand = ""
            if startDate and endDate is not None:
                dateCommand = "AND date_time >= '{}' and date_time <= '{}'".format(startDate, endDate)
                command = command + dateCommand

            data_temp = [];
            i = 0;
            for cond in conds:
                data_temp.append(dict_historical_data(cond.tickers,cond.queryType,cond.startDate,cond.endDate))
                if cond.direction == "greater":
                    if cond.param0 == "average":
                        command += "AND open > (SELECT AVG(open) FROM data_temp[{}]).format(i)
                    if cond.param0 == "low":
                        command += "AND open > (SELECT MIN(open) FROM data_temp[{}]).format(i)
                    if cond.param0 == "high":
                        command += "AND open > (SELECT MAX(open) FROM data_temp[{}]).format(i)
                if cond.direction == "less":
                    if cond.param0 == "average":
                        command += "AND open > (SELECT AVG(open) FROM data_temp[{}]).format(i)
                    if cond.param0 == "low":
                        command += "AND open > (SELECT MIN(open) FROM data_temp[{}]).format(i)
                    if cond.param0 == "high":
                        command += "AND open > (SELECT MAX(open) FROM data_temp[{}]).format(i)

            command = command + ";"
            data = {}
            data["ticker"] = ticker
            data["queryType"] = queryType
            data["quotes"] = []

            cur = conn.cursor()
            for row in cur.execute(command, (ticker, )):
                quotes = {}
                quotes["date-time"] = row[2]
                quotes["open"] = row[3]
                quotes["high"] = row[4]
                quotes["low"] = row[5]
                quotes["close"] = row[6]
                quotes["volume"] = row[7]
                data["quotes"].append(quotes)

            cur.close()
            ticker_data.append(data)
            
        return ticker_data

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

# Function returns JSON object of 100 quotes with the interval being 1 minute between each quote
def parseRealTimeJSON(symbol, api_key):
    params = {'function' : 'TIME_SERIES_INTRADAY', 'symbol' : symbol, 'interval' : '1min', 'apikey' : api_key}
    URL = 'https://www.alphavantage.co/query'
    r = requests.get(URL, params)
    data = r.json()

    return data

def json_realtime_data(ticker):
    ticker = str(ticker)
    conn = None
    try:
        conn = get_db()
        command = '''SELECT * FROM quotes WHERE date-time >= date('now', '-1 days') AND date-time < date('now);'''
        data = {}
        data["ticker"] = ticker
        data["historical"] = True
        data["quotes"] = []

        cur = conn.cursor()
        for row in cur.execute(command, (ticker, )):
            quotes = {}
            quotes["date-time"] = row[2]
            quotes["open"] = row[3]
            quotes["high"] = row[4]
            quotes["low"] = row[5]
            quotes["close"] = row[6]
            quotes["volume"] = row[7]
            data["quotes"].append(quotes)

        cur.close()
        conn.close()

        jsonData = jsonify(data)
            
        return jsonData

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

from sklearn.svm import SVC
@bp.route('/svm_predict')
def svm_predict():
    tickers = ["GOOG"]
    queryType = "history"
    startDate = "2019-01-20"
    endDate = "2019-04-20"
    raw_data = dict_historical_data(tickers, queryType, startDate, endDate)[0]["quotes"]
    raw_data = np.array([elem["open"] for elem in raw_data]).reshape(-1, 1)
    print("Printing entries!")
    # print(raw_data[0])
    for elem in raw_data:
        print(elem)
    X = raw_data
    y = [1 if X[i + 1] >= X[i] else 0 for i in range(len(X) - 1)] + [1]
    clf = SVC(gamma='auto')
    clf.fit(X, y)
    result = clf.predict([X[-1]])
    print("Hello")
    print("The result is {}".format(result[0]))
    return str(result[0])

@bp.route('/neural_predict')
def neural_predict():
    data = np.asarray([[1,2,3],[4,5,6]])
    labels = np.asarray([[1],[2]])
    predictor = nn.LongTermPredictor(data)
    predictor.trainModel(data,labels)
    return str(predictor.predictPoint(data)[0])

@bp.route('/bayesian_predict')
def bayesian_predict():
    print("Hello")
    return "4321"

if __name__ == "__main__":
    bp.run(debug = True)