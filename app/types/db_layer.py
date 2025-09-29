# app/types/db_layer.py
"""
Database layer types.
"""
import sqlite3
from typing import Optional

# == Database connection custom Type alias ==
DatabaseConnection = Optional[sqlite3.Connection]
