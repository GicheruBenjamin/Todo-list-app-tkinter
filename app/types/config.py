# app/types/config.py
"""
Config types.
~ App settings
~ Database settings
~ Theme settings
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


@dataclass
class AppInfo:
    """
    App settings.
    """
    app_name: str                  # Application name
    version: str                   # Application version
    author: str                    # Author name
    window_title: str              # Window title for Tkinter
    description: str               # Short app description
    window_size: tuple[int, int]   # (width, height) of the main window
    icon_path: Path                # Path to application icon (relative or absolute)


@dataclass
class DatabaseSettings:
    """
    Database settings for the app (using SQLite).
    """
    db_path: Path                  # Path to SQLite database file
    db_name: str                   # Database logical name
    db_timeout: int                # Timeout (seconds) for DB connections


class FontWeight(Enum):
    """
    Font weight options.
    """
    NORMAL = "normal"
    BOLD = "bold"
    LIGHT = "light"


@dataclass
class Theme:
    """
    Theme configuration for the application UI.
    """
    theme_name: str                # Name of the theme (e.g., Light, Dark)

    # Colors
    primary_color: str             # Main accent color
    bg_color: str                  # Background color
    text_color: str                # Primary text color
    bordercolor: str               # Border color
    hover_color: str               # Hover state background color

    # Typography
    font_family: str               # Font family (e.g., Arial, Roboto)
    font_size: int                 # Default font size
    font_weight: FontWeight        # Font weight (Enum: NORMAL, BOLD, LIGHT)
