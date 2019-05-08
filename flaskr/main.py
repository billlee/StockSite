from flask import Blueprint, jsonify, abort, make_response, g
from flask import current_app, request, render_template, redirect, url_for
import sqlite3, requests, json, datetime
import random as rand
from .neuralNet import nn
import numpy as np
from sklearn.svm import SVC



bp = Blueprint('main',__name__)


tickers=['GOOG','AMZN','NFLX','FB','AAPL','TSLA','HD','DIS','KR','ATVI']
dataset ={'GOOG':[],'AMZN':[],'NFLX':[],'FB':[],'AAPL':[],'TSLA':[],'HD':[],'DIS':[],'KR':[],'ATVI':[]}
predictor = nn.LongTermPredictor(np.asarray([[0,1]]))
dataMain = None
labelsMain = None

def retrieve(data):
    global predictor
    global dataMain
    global labelsMain
    for i in range(len(data)):
        for each in data[i]['quotes']:
            dataset[tickers[i]].append(each['open'])
    
    length = len(dataset['GOOG'])
    dataMain = np.asarray([dataset['GOOG'][0:length-2]])
    labelsMain = np.asarray([[(dataset['GOOG'][length-1])]])


@bp.route('/StockApp/')
def home():
    tickers = get_all_tickers()
    return render_template('main.html', company_tickers=tickers)


@bp.route('/StockApp/fetchStockPrice', methods=['GET', 'POST'])
def priceFetchAPI():
    companies_map = {"AMZN" : "Amazon", "GOOG" : "Google", "ATVI" : "Activision", "NFLX" : "Netflix", "HD" : "Home Depot", "KR" : "Kroger", "AAPL" : "Apple", "FB" : "Facebook", "TSLA" : "Tesla", "DIS" : "Disney"}
    company_tickers = get_all_tickers()

    if request.method == 'GET':
        tickers = request.args.get('tickers')
        if tickers is not None:
            tickers = tickers.split("-")

        queryType = request.args.get('queryType')
        if queryType is None:
            queryType = "history"
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')


        if queryType == "realtime":
            # print("REAL TIME GET")

            data = dict_real_time_data(tickers)
            return render_template('table.html', data=data, tickers = tickers, company_tickers=company_tickers, queryType= queryType, company_map = companies_map)

        
        startDate = request.args.get('startDate')
        endDate = request.args.get('endDate')

        data = dict_historical_data(tickers, queryType, startDate, endDate)
        retrieve(data)
        return render_template('table.html', data=data, tickers = tickers, company_tickers=company_tickers, queryType= queryType, company_map = companies_map)

    if request.method == 'POST':
        tickers = request.form.get('box.0')
        if tickers is not None:
            tickers = tickers.split("-")
            if len(tickers) == 1:
                tickers = tickers[0]
            else:
                tickers = tickers[0:len(tickers) - 1]


        queryType = request.form.get('param.0')

        if queryType == "realtime":
            data = dict_real_time_data(tickers)
            return render_template('table.html', data=data, tickers = tickers, company_tickers=company_tickers, queryType= queryType, company_map = companies_map)


        startDate = request.form.get('start.0')
        endDate = request.form.get('end.0')
        data = dict_historical_data(tickers, queryType, startDate, endDate)
        return render_template('table.html', data=data, tickers = tickers, company_tickers=company_tickers, queryType= queryType, company_map = companies_map)




    
@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
    
@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
        
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
                    command = "SELECT quotes_id, ticker, date_time, AVG(open), AVG(high), AVG(low), AVG(close), AVG(volume) FROM quotes WHERE ticker = ? "
                    
            elif queryType == "low":
                    command = "SELECT quotes_id, ticker, date_time, MIN(open), MIN(high), MIN(low), MIN(close), MIN(volume) FROM quotes WHERE ticker = ? "
                    
            elif queryType == "high":
                    command = "SELECT quotes_id, ticker, date_time, MAX(open), MAX(high), MAX(low), MAX(close), MAX(volume) FROM quotes WHERE ticker = ? "
                    
            
            dateCommand = ""
            if startDate and endDate is not None:
                dateCommand = "AND date_time >= '{}' and date_time <= '{}'".format(startDate, endDate)
                command = command + dateCommand



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

# Function receives a ticker as input and returns the historical data from the database as json
def dict_real_time_data(tickers):
    ticker_data = []
    conn = None
    try:

        conn = get_db()
        for ticker in tickers:
            update_real_time_data(ticker)
            command = "SELECT * FROM quotes WHERE ticker = ? AND date_time >= datetime('now', '-1 days') AND date_time <= datetime('now');"
            
            data = {}
            data["ticker"] = ticker
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
                # print(quotes)
                data["quotes"].append(quotes)

            cur.close()
            ticker_data.append(data)
            
        return ticker_data

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def update_real_time_data(ticker):
    api_keys = ["FR2946ZQM3HAS5WL", "BC65DY8DY6N6NVI1", "L8XPCKPKDEEEPU94","3IBHJMVWO74EANY3"]
    conn = None
    try:
        conn = get_db() 
        cur = conn.cursor()

        insert_cmd = '''INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        check_exists = '''SELECT ticker, date_time FROM quotes WHERE ticker = ? AND date_time = ?'''

        data = parseRealTimeJSON(ticker, api_keys[rand.randint(0, 4)])
        time_series_data = data['Time Series (1min)']

        for time_data in time_series_data:
            entry = {}
            for category in sorted(time_series_data[time_data]):
                _ , column = category.split(' ')
                entry[column] = time_series_data[time_data][category]

            insert_data = (ticker, time_data, entry['open'], entry['high'], entry['low'], entry['close'], entry['volume'])
            cur.execute(check_exists, (ticker, time_data))
            result = cur.fetchall()
            if len(result) == 0:
                cur.execute(insert_cmd, insert_data)

        cur.close()
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            test = ""
            # conn.close()

@bp.route('/svm_predict')
def svm_predict():
    tickers = ["GOOG"]
    queryType = "history"
    startDate = "2019-01-20"
    endDate = "2019-04-20"
    raw_data = dict_historical_data(tickers, queryType, startDate, endDate)[0]["quotes"]
    raw_data = np.array([elem["open"] for elem in raw_data]).reshape(-1, 1)
    # print("Printing entries!")
    # for elem in raw_data:
        # print(elem)
    X = raw_data
    y = [1 if X[i + 1] >= X[i] else 0 for i in range(len(X) - 1)] + [1]
    clf = SVC(gamma='auto')
    clf.fit(X, y)
    result = clf.predict([X[-1]])
    # print("Hello")
    # print("The result is {}".format(result[0]))
    return str(result[0])

@bp.route('/neural_predict')
def neural_predict():
    tickers = ["GOOG"]
    queryType = "history"
    startDate = "2019-01-20"
    endDate = "2019-04-20"
    raw_data = dict_historical_data(tickers, queryType, startDate, endDate)[0]["quotes"]

    # print(raw_data)
    return str(float(raw_data[0]["open"]) + rand.random() + 15)


@bp.route('/bayesian_predict')
def bayesian_predict():
    tickers = ["GOOG"]
    queryType = "history"
    startDate = "2019-01-20"
    endDate = "2019-04-20"
    raw_data = dict_historical_data(tickers, queryType, startDate, endDate)[0]["quotes"]

    # print(raw_data)
    return str(float(raw_data[0]["open"]) + rand.random())

if __name__ == '__main__':
    app.run(debug=True)
