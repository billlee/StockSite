# written by: Kendric Postrero
# assisted by: Anton Maliev
# debugged by: Bill Lee
import data_parser
import psycopg2
import time
import sys

# Function uploads the real time data into the table
def realTimeParse(symbol, is_second):
	conn = psycopg2.connect("host='localhost' dbname='demo' user='demo' password='test'")    
	cur = conn.cursor()

	api_key = 'FR2946ZQM3HAS5WL'
	data = data_parser.parseRealTimeJSON(symbol, api_key)
	time_series_data = data['Time Series (1min)']

	insert_cmd = "INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
	check_exists = "SELECT ticker, date_time FROM quotes WHERE ticker = %s AND date_time = %s"

	for time_data in reversed(sorted(time_series_data.keys())):
		entry = {}
		for category in sorted(time_series_data[time_data]):
			_ , column = category.split(' ')
			entry[column] = time_series_data[time_data][category]
		insert_data = (symbol, time_data, entry['open'], entry['high'], entry['low'], entry['close'], entry['volume'])
		cur.execute(check_exists, (symbol, time_data))
		result = cur.fetchall()
		if len(result) == 0:
			cur.execute(insert_cmd, insert_data)
		if is_second:
			print(insert_data)
			break

	conn.commit()


if __name__ == '__main__':

	user_input = str(sys.argv[1])

	realTimeParse(user_input, False)

	while True:
		time.sleep(15)
		realTimeParse(user_input, True)
