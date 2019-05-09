# written by: Kendric Postrero
# assisted by: Anton Maliev
# debugged by: Bill Lee
import psycopg2
import data_parser
import time

# Function intializes table in a new database
def createTables():
    commands = (
        """
        CREATE TABLE companies (
            ticker VARCHAR(5) PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            industry VARCHAR(50) NOT NULL
        )
        """,
        """ CREATE TABLE quotes (
                quotes_id SERIAL PRIMARY KEY,
                ticker VARCHAR(5) NOT NULL,
                date_time timestamp NOT NULL,
                open REAL NOT NULL,
                high REAL NOT NULL,
                low REAL NOT NULL, 
                close REAL NOT NULL,
                volume BIGINT NOT NULL,
                FOREIGN KEY (ticker)
                REFERENCES companies (ticker)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # Connect to the PostgreSQL server
        conn = psycopg2.connect("host='localhost' dbname='demo' user='demo' password='test'")

        # Get cursor to use database
        cur = conn.cursor()

        # Create each table
        for command in commands:
            cur.execute(command)

        # Close communication with the PostgreSQL database server
        cur.close()

        # Commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Function intializes the company table
def initCompaniesTable():

    conn = None
    try:

        conn = psycopg2.connect("host='localhost' dbname='demo' user='demo' password='test'")
            
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


        command = "INSERT INTO companies (ticker, name, industry) VALUES (%s, %s, %s)"

        for company in companies:
            cur.execute(command, company)

        cur.close()
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# Function gets the weekly historic data of our company based on the company table
def initHistoricData():
    api_key = 'FR2946ZQM3HAS5WL'
    conn = None
    try:
        conn = psycopg2.connect("host='localhost' dbname='demo' user='demo' password='test'")    
        cur = conn.cursor()
        query = "SELECT ticker FROM companies"
        cur.execute(query)
        result = cur.fetchall()
        tickers = []
        for t in result:
            tickers.append(t)

        insert_cmd = "INSERT INTO quotes (ticker, date_time, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        check_exists = "SELECT ticker, date_time FROM quotes WHERE ticker = %s AND date_time = %s"

        for ticker in tickers:
            data = data_parser.parseWeeklyJSON(ticker, api_key)

            time_series_data = data['Weekly Time Series']

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

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# Initialize the database
if __name__ == '__main__':
    createTables()
    initCompaniesTable()
    # initHistoricData()


