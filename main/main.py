# Run db_schema.sql in mysql first to generate the database

from scripts.download_data import download_data
from scripts.import_data import import_data
from scripts.get_price_data import get_price_data
# from scripts import import_supplementary_data
from datetime import datetime
import getpass

# Download, import, and collect price data in one script
def main():
    start_year = 2009,
    start_qtr = 1,
    end_year = (datetime.now().year - 1),
    end_qtr = 4,
    output_dir = "../edgar_data"
    cik_to_tick = pd.read_json('../other_data/CIK_to_company_tickers.json'), 
    price_data_output_dir = '../other_data/'

    db = {}
    db["host"] = "localhost"
    db["port"] = 3306
    db["user"] = "root"
    db["db_name"] = "edgar"
    db["password"] = getpass.getpass("Database password: ")

    download_data(start_year, start_qtr, end_year, end_qtr, output_dir)
    import_data(db, output_dir, start_year, start_qtr, end_year, end_qtr)

    get_price_data(start=datetime(start_year, start_qtr * 4, 1).strftime('%Y-%m-%d'),
                   end=datetime(end_year, end_qtr * 4, 1).strftime('%Y-%m-%d'),
                   cik_to_tick=cik_to_tick, 
                   output_dir=price_data_output_dir)

if __name__ == "__main__":
    main()