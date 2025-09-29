# app/db/sqlitte_db.py
import sqlite3
from .migration_ddl import MIGRATION_DDL
from app.types import DatabaseSettings
from app.types.db_layer import DatabaseConnection

class SqliteDb:
    """
    SQLite database wrapper that manages connection and migrations.
    """
    def __init__(self, db_settings: DatabaseSettings):
        self.db_settings = db_settings
        self.connection: DatabaseConnection | None = None

    def connect(self) -> DatabaseConnection | None:
        """Connect to the database and run migrations."""
        try:
            self.connection = sqlite3.connect(
                self.db_settings.db_path,
                timeout=self.db_settings.db_timeout,
                check_same_thread=False
            )
            cursor = self.connection.cursor()
            try:
                for ddl in MIGRATION_DDL:
                    cursor.executescript(ddl)
                self.connection.commit()
            finally:
                cursor.close()
            return self.connection
        except sqlite3.Error as e:
            print(f"[DB ERROR] Failed to connect or run migrations: {e}")
            self.connection = None
            return None

    def close(self) -> bool:
        """Close the database connection safely."""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                return True
            except sqlite3.Error as e:
                print(f"[DB ERROR] Failed to close connection: {e}")
        return False
