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
    app_name : str 
    version : str 
    author : str 
    window_title : str 
    description : str 
    window_size : tuple 

@dataclass
class Databasesettings:
    # Database settings for the app
    # Using SQLite
    db_path : str 
    db_name : str
    db_timeout : int

@dataclass
class Theme:
    # A theme 
    theme_name : str 
    # Colors
    primary_color : str 
    bg_color : str 
    text_color : str 
    bordercolor : str 
    hover_color : str 
    # Typography
    font_family : str 
    font_size : int 
    font_weight : str 


