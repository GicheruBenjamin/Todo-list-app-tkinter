# app/types/config.py
"""
Config types.
~ App settings
~ Database settings
~ Theme settings
"""

from dataclasses import dataclass
from enum import Enum

@dataclass
class AppInfo:
    """
    App settings.
    """
    app_name : str 
    version : str 
    author : str 
    window_title : str 
    description : str 
    window_size : tuple 
    icon_path : str

@dataclass
class DatabaseSettings:
    # Database settings for the app
    # Using SQLite
    db_path : str 
    db_name : str
    db_timeout : int

class FontWeight(Enum):
    """
    Font weight
    """
    NORMAL = "normal"
    BOLD = "bold"
    LIGHT = "light"

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


