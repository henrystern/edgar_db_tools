# Generate the database by running the ../SQL scripts first

from datetime import datetime
import requests
import zipfile
import io
import os.path

import yfinance as yf
import pandas as pd
from ratelimit import limits, sleep_and_retry

from utils import get_db_credentials, connect_to_db

# Download and extract EDGAR datasets over a specified period


def download_edgar_data(start_year=2009,
                  start_qtr=1,
                  end_year=(datetime.now().year - 1),
                  end_qtr=4,
                  output_dir="./edgar_data/"):

    for year in range(start_year, end_year + 1):
        for q in range(start_qtr, 4 + 1):
            if year == end_year and q == end_qtr + 1:
                break
            period = str(year) + "q" + str(q)
            print(f'{datetime.now():%m-%d %H:%M:%S}', "Downloading", period)
            u = "https://www.sec.gov/files/dera/data/financial-statement-data-sets/" + period + ".zip"
            r = requests.get(u, stream=True)
            print(f'{datetime.now():%m-%d %H:%M:%S}', "Extracting", period)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            z.extractall(output_dir + period)
        start_qtr = 1

# Import EDGAR datasets into the MySQL database


def import_edgar_data(db=None,
                data_dir="./edgar_data/",
                start_year=2009,
                start_qtr=1,
                end_year=(datetime.now().year - 1),
                end_qtr=4):

    # Generate the import command for execution by the cursor
    def generate_command(path, year, qtr, file, extension, db_name):
        file_path = path + str(year) + "q" + str(qtr) + "/" + file + extension
        print(f'{datetime.now():%m-%d %H:%M:%S}', "Importing", file_path)
        sql_command = ("LOAD DATA LOCAL INFILE '"
                       + file_path
                       + "' IGNORE INTO TABLE `" + db_name + "`.`" + file
                       + "` CHARACTER SET utf8mb4 FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\n' IGNORE 1 LINES;")
        return sql_command

    db = get_db_credentials(db)

    connection = connect_to_db(db)

    if not connection:
        return

    cursor = connection.cursor()

    files = ["sub", "tag", "num", "pre"]

    for year in range(start_year, end_year + 1):
        for qtr in range(start_qtr, 4 + 1):
            if year == end_year and qtr == end_qtr + 1:
                break
            for file in files:
                sql_command = generate_command(
                    data_dir, year, qtr, file, ".txt", db["db_name"])
                cursor.execute(sql_command)
                connection.commit()
        start_qtr = 1
        year += 1

    cursor.close()
    connection.close()

# Get Yahoo Finance OHLCV for each ticker


def get_price_data(start=datetime(2009, 1, 1).strftime('%Y-%m-%d'),
                   end=datetime.today().strftime('%Y-%m-%d'),
                   frequency='1d',  # see yfinance docs
                   data='./other_data/CIK_to_company_tickers.json',
                   output_dir='./other_data/',
                   output_name='price_data.csv'):

    cik_to_tick = pd.read_json(data).T
    num_tickers = len(cik_to_tick) - 1
    for i, (cik, ticker, company) in cik_to_tick.iterrows():
        print(f"{i + 1} out of {num_tickers}:", company, ticker)

        # max 2000 requests per hour
        check_api_limit()

        stock_data = yf.download(ticker, start, end, interval=frequency)
        stock_data.insert(0, 'Ticker', ticker)
        stock_data.insert(0, 'Company', company)
        stock_data.insert(0, 'CIK', cik)

        if not os.path.exists(output_dir + output_name):
            stock_data.to_csv(output_dir + output_name, header=True)
        else:
            stock_data.to_csv(output_dir + output_name, header=False, mode="a")


# Limit calls to comply with Yahoo Finance API limit
@sleep_and_retry
@limits(calls=2000, period=3600)
def check_api_limit():
    ...

# Import price data into MySQL table 'price'


def import_price_data(db=None, data="./other_data/price_data.csv"):

    db = get_db_credentials(db)
    connection = connect_to_db(db)

    if not connection:
        return

    cursor = connection.cursor()

    print(f'{datetime.now():%m-%d %H:%M:%S}', "Importing", data)
    sql_command = ("LOAD DATA LOCAL INFILE '" + data
                   + "' IGNORE INTO TABLE `" + db["db_name"] + "`.`price`"
                   + " CHARACTER SET utf8mb4 FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES;")

    cursor.execute(sql_command)
    connection.commit()

    cursor.close()
    connection.close()

def import_supplementary_data():
    ...

# If run as a script do everything in one step
# Modify these values as needed
if __name__ == "__main__":
    start_year = 2022
    start_qtr = 2
    end_year = datetime.now().year - 1
    end_qtr = 3
    output_dir = "./edgar_data/"
    ticker_data = './other_data/CIK_to_company_tickers.json'
    price_data_output_dir = './other_data/'
    price_data_output_name = 'price_data.csv'

    db = {}
    db["host"] = "localhost"
    db["port"] = 3306
    db["user"] = "root"
    db["db_name"] = "edgar"

    db = get_db_credentials(db)

    connection = connect_to_db(db)

    if not connection:
        exit()

    connection.close()

    # download_edgar_data(start_year, start_qtr, end_year, end_qtr, output_dir)
    # import_edgar_data(db, output_dir, start_year, start_qtr, end_year, end_qtr)

    # get_price_data(start=datetime(start_year, start_qtr * 4, 1).strftime('%Y-%m-%d'),
    #                end=datetime(end_year, end_qtr * 4, 1).strftime('%Y-%m-%d'),
    #                data=ticker_data,
    #                output_dir=price_data_output_dir,
    #                output_name=price_data_output_name)

    import_price_data(db, price_data_output_dir + price_data_output_name)
