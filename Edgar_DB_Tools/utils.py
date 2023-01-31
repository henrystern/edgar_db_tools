import mysql.connector
import getpass

def get_db_credentials(db):
        print("Input Database Credentials")
        if "host" not in db:
            db["host"] = input("Host: (localhost)") or "localhost"
        if "port" not in db:
            db["port"] = input("Port: (3306)") or "port"
        if "user" not in db:
            db["user"] = input("User: (root)") or "root" 
        if "db_name" not in db:
            db["db_name"] = input("Database name: (edgar)") or "edgar"
        if "password" not in db:
            db["password"] = getpass.getpass("Database password: ")
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