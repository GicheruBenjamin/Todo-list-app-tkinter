# app/config/load_db_settings.py
"""
Load database settings.
"""

from pathlib import Path
from app.types import DatabaseSettings

def load_db_settings() -> DatabaseSettings:
    """
    Load database settings.
    """
    database_path = Path("data/todie.db")  # now Path instead of str
    database_name = "todie"
    database_timeout = 30
    return DatabaseSettings(
        db_path=database_path,
        db_name=database_name,
        db_timeout=database_timeout
    )
