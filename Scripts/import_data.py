# requires "pip install mysql-connector-python"

from datetime import datetime
import getpass
import mysql.connector

def import_data(db=None,
                data_dir="../data",
                start_year=2009,
                start_qtr=1,
                end_year=(datetime.now().year - 1),
                end_qtr=4):

    if db == None:
        db = get_db_credentials()

    if "password" not in db:
        db["password"] = getpass.getpass("Database password: ")

    connection = connect_to_db(db)

    if not connection:
        return

    cursor = db.cursor()

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
        db["host"] = input("Host: ") or "localhost"
        db["user"] = input("User: ") or "root" 
        db["db_name"] = input("Database name: ") or "edgar"
        return db

def connect_to_db(db):
    try:
        database_connection = mysql.connector.connect(user=db["username"],
                                     password=db["password"],
                                     host=db["host"],
                                     database=db["db_name"],
                                     allow_local_infile=True)
        return database_connection
    except:
        print("Can't connect to database")
        return None

def generate_command(path, year, qtr, file, extension, db_name):
    file_path = path + str(year) + "q" + str(qtr) + "/" + file + extension

    print(f'{datetime.now():%m-%d %H:%M:%S}', file_path)

    sql_command = ("LOAD DATA LOCAL INFILE '"
                   + file_path
                   + "' IGNORE INTO TABLE `" + db_name + "`.`" + file
                   + "` CHARACTER SET utf8mb4 FIELDS TERMINATED BY '\\t' LINES TERMINATED BY '\\n' IGNORE 1 LINES;")
    print(sql_command)
    return sql_command


if __name__ == "__main__":
    import_data()