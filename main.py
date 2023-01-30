# Run db_schema.sql in mysql first to generate the database

from Edgar_DB_Tools.download_data import download_data
from Edgar_DB_Tools.import_data import import_data, connect_to_db
from Edgar_DB_Tools.get_price_data import get_price_data
# from Edgar_DB_Tools.import_supplementary_data import import_supplementary_data
from datetime import datetime
import getpass

# Download, import, and collect price data in one script
def main():
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
    db["password"] = getpass.getpass("Database password: ")

    connection = connect_to_db(db)

    if not connection:
        return

    connection.close()

    download_data(start_year, start_qtr, end_year, end_qtr, output_dir)
    import_data(db, output_dir, start_year, start_qtr, end_year, end_qtr)

    get_price_data(start=datetime(start_year, start_qtr * 4, 1).strftime('%Y-%m-%d'),
                   end=datetime(end_year, end_qtr * 4, 1).strftime('%Y-%m-%d'),
                   data=ticker_data, 
                   output_dir=price_data_output_dir,
                   output_name=price_data_output_name)

if __name__ == "__main__":
    main()