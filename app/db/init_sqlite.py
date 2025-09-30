# app/db/init_sqlite.py (init_sqlite)
"""
SQLite initialization and migration.
"""

import sqlite3
import logging
from app.types import DatabaseSettings, DatabaseConnection
from .migration_ddl import MIGRATION_DDL


def init_sqlite(db_settings: DatabaseSettings) -> DatabaseConnection:
    """
    Initialize the sqlite database and run migrations.
    """
    try:
        connection = sqlite3.connect(
            str(db_settings.db_path),
            timeout=db_settings.db_timeout,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        cursor = connection.cursor()

        # Run migrations
        for ddl in MIGRATION_DDL:
            cursor.executescript(ddl)

        connection.commit()
        return connection

    except Exception as e:
        logging.error("SQLite initialization failed", exc_info=True)
        return None


def close_sqlite(connection: DatabaseConnection) -> bool:
    """
    Close the sqlite database connection safely.
    """
    try:
        if connection:
            connection.close()
            return True
        return False
    except Exception as e:
        logging.error("Failed to close SQLite connection", exc_info=True)
        return False
