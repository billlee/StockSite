import requests

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

