# app/main.py

# == Entry point ==
from app.config import provide_app_settings, provide_theme_settings, load_db_settings
from app.db import init_sqlite, close_sqlite

def main():
    app_settings = provide_app_settings()
    theme_settings = provide_theme_settings()
    db_settings = load_db_settings()

    print(app_settings)
    print(theme_settings)
    print(db_settings)

    connection = init_sqlite(db_settings)
    print(connection)
    close_sqlite(connection)




if __name__ == "__main__":
    main()