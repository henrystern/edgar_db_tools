import yfinance as yf
import pandas as pd
from datetime import datetime
import os.path
from ratelimit import limits, sleep_and_retry

# Get Yahoo Finance OHLCV for each ticker
def get_price_data(start=datetime(2009, 1, 1).strftime('%Y-%m-%d'),
                   end=datetime.today().strftime('%Y-%m-%d'),
                   frequency='1wk',  # see yfinance docs
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


@sleep_and_retry
@limits(calls=2000, period=3600)
def check_api_limit():
    ...

if __name__ == "__main__":
    get_price_data()
