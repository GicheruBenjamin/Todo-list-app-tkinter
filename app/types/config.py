# app/types/config.py
"""
Config types.
~ App settings
~ Database settings
~ Theme settings
"""

from dataclasses import dataclass

@dataclass
class Appinfo:
    """
    App settings.
    """
    app_name : str = "Todoie"
    version : str = "0.1.0"
    author : str = "Gicheru Benjamin"
    window_title : str = "Todoie"
    description : str = "A simple todo list app"
    window_size : tuple = (800, 600)

@dataclass
class Databasesettings:
    # Database settings for the app
    # Using SQLite
    db_path : str = "/data/todoie.db"
    db_name : str = "todoie"
    db_timeout : int = 30

@dataclass
class Theme:
    # A theme 
    theme_name : str = "light"
    # Colors
    primary_color : str = "#007bff"
    bg_color : str = "#ffffff"
    text_color : str = "#000000"
    bordercolor : str = "#ced4da"
    hover_color : str = "#007bff"
    # Typography
    font_family : str = "Arial"
    font_size : int = 14
    font_weight : str = "normal"


