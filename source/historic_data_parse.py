import data_parser
import database
import psycopg2
import sys

# Function uploads the historic data into the table
def addHistoricData(symbol):  
    api_key = 'FR2946ZQM3HAS5WL'
    conn = None
    try:
        conn = psycopg2.connect("host='localhost' dbname='demo' user='demo' password='test'")    
        cur = conn.cursor()

        insert_cmd = "INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        check_exists = "SELECT ticker, date_time FROM quotes WHERE ticker = %s AND date_time = %s"
        
        data = data_parser.parseWeeklyJSON(symbol, api_key)
        time_series_data = data['Weekly Time Series']

        for time_data in time_series_data:
            entry = {}
            for category in sorted(time_series_data[time_data]):
                _ , column = category.split(' ')
                entry[column] = time_series_data[time_data][category]

            insert_data = (symbol, time_data, entry['open'], entry['high'], entry['low'], entry['close'], entry['volume'])
            cur.execute(check_exists, (symbol, time_data))
            result = cur.fetchall()
            if len(result) == 0:
                cur.execute(insert_cmd, insert_data)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# User inputs a stock ticker and uploads 100 weekly historic quote data
if __name__ == '__main__':

    user_input = str(sys.argv[1])
    addHistoricData(user_input)
