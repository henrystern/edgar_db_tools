# requires "pip install mysql-connector-python"

from datetime import datetime
import getpass
import mysql.connector

# Import datasets into the MySQL database
def import_data(db=None,
                data_dir="../edgar_data",
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


    if db == None:
        db = get_db_credentials()

    if "password" not in db:
        db["password"] = getpass.getpass("Database password: ")

    connection = connect_to_db(db)

    if not connection:
        return

    cursor = connection.cursor()

    files = ["num", "pre", "sub", "tag"]

    for year in range(start_year, end_year + 1):
        for qtr in range(start_qtr, 4 + 1):
            if year == end_year and qtr == end_qtr + 1:
                break
            for file in files:
                sql_command = generate_command(
                    data_dir, year, qtr, file, ".txt", db["db_name"])
                cursor.execute(sql_command)
        start_qtr = 1
        year += 1

    connection.commit()
    cursor.close()
    connection.close()

def get_db_credentials():
        db = {}
        print("Input Database Credentials")
        db["host"] = input("Host: (localhost)") or "localhost"
        db["port"] = input("Port: (3306)") or "port"
        db["user"] = input("User: (root)") or "root" 
        db["db_name"] = input("Database name: (edgar)") or "edgar"
        return db

def connect_to_db(db):
    try:
        database_connection = mysql.connector.connect(user=db["user"],
                                     password=db["password"],
                                     host=db["host"],
                                     port=db["port"],
                                     database=db["db_name"],
                                     allow_local_infile=True)
        return database_connection
    except:
        print("Can't connect to database")
        return None

if __name__ == "__main__":
    import_data()