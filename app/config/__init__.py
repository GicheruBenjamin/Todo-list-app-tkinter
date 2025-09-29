# app/config/__init__.py
"""
Config module.
"""
from .load_db_settings import load_db_settings
from .provide_app_settings import provide_app_settings
from .provide_theme_settings import provide_theme_settings
#out modules 
from app.types import AppInfo, DatabaseSettings, Theme
# in modules
from dataclasses import dataclass

@dataclass
class AppConfig:
    app_info : AppInfo
    db_settings : DatabaseSettings
    theme : Theme

def provide_app_config() -> AppConfig:
    """
    Provide app config.
    """
    app_info = provide_app_settings()
    db_settings = load_db_settings()
    theme = provide_theme_settings()
    return AppConfig(
        app_info = app_info,
        db_settings = db_settings,
        theme = theme
    )


__all__ = [
    "AppConfig",
    "provide_app_config",
]