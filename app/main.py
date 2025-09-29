# app/main.py

# == Entry point ==
from app.db import SqliteDb
from app.config import provide_app_config, AppConfig

def main():
    ac : AppConfig = provide_app_config()
    db : SqliteDb = SqliteDb(ac.db_settings)
    db.connect()
    if db.connection:
        print("Connected to the database")
        print(db.connection)
        db.close()
    else:
        print("Failed to connect to the database")



if __name__ == "__main__":
    main()