import yfinance as yf
import pandas as pd
from datetime import datetime
import time

# Get Yahoo Finance price data for each ticker
def get_price_data(start=datetime(2009, 1, 1).strftime('%Y-%m-%d'), 
                   end=datetime.today().strftime('%Y-%m-%d'), 
                   frequency='1wk', # see yfinance docs 
                   cik_to_tick=pd.read_json('../other_data/CIK_to_company_tickers.json'), 
                   output_dir='../other_data/'):

    cik_to_tick = cik_to_tick[(cik_to_tick.company_name != "''")]

    price = pd.DataFrame()

    progress = 1

    num_tickers = len(cik_to_tick)

    for i in range(0, num_tickers):
        ticker = cik_to_tick.ticker.iloc[i]
        print(ticker)
        if (i/len(cik_to_tick))*100 > progress:
            print(progress, '%')
            progress = progress + 1
            if progress % 10 == 0:
                # Save some progress in case there's an error
                price.to_csv(output_dir + 'price_data.csv', index=False)
        raw_data = yf.download(ticker, start, end, interval=frequency)
        stock_data = pd.DataFrame(
            columns=['ticker', 'cik', 'date', 'price', 'volume'])
        stock_data.price = raw_data.Close
        stock_data.volume = raw_data.Volume
        stock_data.date = raw_data.index
        stock_data.ticker = ticker
        price = price.append(stock_data)
        time.sleep(2)  # max 2000 requests per hour

    # 10,000 tickers will take 5.5 hours to complete

    price.to_csv(output_dir + 'price_data.csv', index=False)

if __name__ == "__main__":
    get_price_data()