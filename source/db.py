import sqlite3

import click
from flask import current_app, g, jsonify
from flask.cli import with_appcontext
from .neuralNet import nn

import requests
import time


# Function returns JSON object of 100 quotes with the interval being 1 minute between each quote
def parseRealTimeJSON(symbol, api_key):
    params = {'function' : 'TIME_SERIES_INTRADAY', 'symbol' : symbol, 'interval' : '1min', 'apikey' : api_key}
    URL = 'https://www.alphavantage.co/query'
    r = requests.get(URL, params)
    data = r.json()

    return data

# Function returns JSON object of 100 quotes with the interval being 1 week between each quote
def parseWeeklyJSON(symbol, api_key):
    params = {'function' : 'TIME_SERIES_WEEKLY', 'symbol' : symbol, 'apikey' : api_key}
    URL = 'https://www.alphavantage.co/query'
    r = requests.get(URL, params)
    data = r.json()

    return data


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def train_neural_network():
    '''
    pretrains the neural network into a pickle
    '''
    tickers=['GOOG','AMZN','NFLX','FB','AAPL','TSLA','HD','DIS','KR','ATVI']
    dataset ={'GOOG':[],'AMZN':[],'NFLX':[],'FB':[],'AAPL':[],'TSLA':[],'HD':[],'DIS':[],'KR':[],'ATVI':[]}
    predictor = nn.LongTermPredictor(np.asarray([[0,1]]))
    for i in range(len(data)):
        for each in data[i]['quotes']:
            dataset[tickers[i]].append(each['open'])
    
    length = len(dataset['GOOG'])
    dataMain = np.asarray([dataset['GOOG'][0:length-2]])
    labelsMain = np.asarray([[(dataset['GOOG'][length-1])]])


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def init_companies():
    db = get_db()

    conn = None
    try:

        conn = get_db()
            
        cur = conn.cursor()

        companies = [("GOOG", "Alphabet Inc.", "Internet Content & Information"),
        ("AMZN", "Amazon.com, Inc.", "Specialty Retail"),
        ("NFLX", "Netflix, Inc.", "Media - Diversified"),
        ("FB", "Facebook, Inc.", "Internet Content & Information"),
        ("AAPL", "Apple Inc.", "Consumer Electronics"),
        ("TSLA", "Tesla, Inc.", "Auto Manufacturers"),
        ("HD", "The Home Depot, Inc.", "Home Improvement Stores"),
        ("DIS", "The Walt Disney Company.", "Media - Diversified"),
        ("KR", "The Kroger Co.", "Grocery Stores"),
        ("ATVI", "Activision Blizzard, Inc.", "Electronic Gaming & Multimedia")]


        command = '''INSERT INTO companies (ticker, name, industry) VALUES (?, ?, ?)'''

        for company in companies:
            cur.execute(command, company)

        cur.close()
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

# Function gets the weekly historic data of our company based on the company table
def init_historical_data():
    api_key = 'FR2946ZQM3HAS5WL'
    conn = None
    try:
        conn = get_db() 
        cur = conn.cursor()

        query = "SELECT ticker FROM companies"
        cur.execute(query)
        result = cur.fetchall()
        tickers = []
        for t in result:
            tickers.append(t[0])

        insert_cmd = '''INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        check_exists = '''SELECT ticker, date_time FROM quotes WHERE ticker = ? AND date_time = ?'''

        for ticker in tickers:
            data = parseWeeklyJSON(ticker, api_key)

            time_series_data = data['Weekly Time Series']

            for time_data in time_series_data:
                entry = {}
                for category in sorted(time_series_data[time_data]):
                    _ , column = category.split(' ')
                    entry[column] = time_series_data[time_data][category]

                insert_data = (ticker, time_data, entry['open'], entry['high'], entry['low'], entry['close'], entry['volume'])
                cur.execute(check_exists, (ticker, time_data + " 00:00:00"))
                result = cur.fetchall()
                if len(result) == 0:
                    cur.execute(insert_cmd, insert_data)
            conn.commit()
            time.sleep(15)

        cur.close()
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

def init_real_time_data():
    api_key = 'FR2946ZQM3HAS5WL'
    conn = None
    try:
        conn = get_db() 
        cur = conn.cursor()

        query = "SELECT ticker FROM companies"
        cur.execute(query)
        result = cur.fetchall()
        tickers = []
        for t in result:
            tickers.append(t[0])

        insert_cmd = '''INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (?, ?, ?, ?, ?, ?, ?)'''
        check_exists = '''SELECT ticker, date_time FROM quotes WHERE ticker = ? AND date_time = ?'''

        for ticker in tickers:
            data = parseRealTimeJSON(ticker, api_key)
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
            conn.commit()
            time.sleep(15)

        cur.close()
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()


# Function prints out companies table in the database to see if it has been properly initialized
def print_tables():
    conn = None
    try:
        conn = get_db()
        command = '''SELECT * FROM companies'''

        cur = conn.cursor()

        # cur.execute(command)
        for row in cur.execute(command):
            print(row[0] + ", ")

        cur.close()



    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

# Function prints out stock information for a certain stock (current initialized for AMZN)
def print_historical_stock_info():
    ticker = "AMZN"
    conn = None
    try:
        conn = get_db()
        command = '''SELECT * FROM quotes WHERE ticker = 'AMZN' '''

        cur = conn.cursor()

        # cur.execute(command)
        for row in cur.execute(command):
            print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) + " " + str(row[3]) + " " + str(row[4]) + " "
                + str(row[5]) + " " + str(row[6]) + " " + str(row[7]))

        cur.close()
        conn.commit()

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()

# Function receives a ticker as input and returns the historical data from the database as json
def json_historical_data(ticker):
    ticker = str(ticker)
    # ticker = "AMZN"
    conn = None
    try:
        conn = get_db()
        command = "SELECT * FROM quotes WHERE ticker = ? ;"
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
        jsonData = jsonify(data)
        conn.commit()


        # For testing purposes
        # for q in data["quotes"]:
        #     print(q)

        return jsonData

    except sqlite3.Error as e:
        print(e)
    finally:
        if conn is not None:
            conn.close()



@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

@click.command('init-companies')
@with_appcontext
def init_companies_command():
    init_companies()
    click.echo('Initialized the companies table')


@click.command('init-historical')
@with_appcontext
def init_historical_command():
    init_historical_data()
    click.echo('Initialized historical stock data for each company')

@click.command('init-real-time')
@with_appcontext
def init_real_time_command():
    init_real_time_data()
    click.echo('Initialized real stock data for each company')


@click.command('print-tables')
@with_appcontext
def init_companies_print():
    print_tables()
    click.echo('printing companies table')

@click.command('print-historical')
@with_appcontext
def init_stock_print():
    print_historical_stock_info()
    click.echo('printing historical stock information')



def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(init_companies_command)
    app.cli.add_command(init_historical_command)
    app.cli.add_command(init_companies_print)
    app.cli.add_command(init_stock_print)
    app.cli.add_command(init_real_time_command)

