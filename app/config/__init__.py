# app/config/__init__.py
"""
App configuration package.
"""

from dataclasses import dataclass

from app.types import AppInfo, DatabaseSettings, Theme

from .load_db_settings import load_db_settings
from .provide_app_settings import provide_app_settings
from .provide_theme_settings import provide_theme_settings


@dataclass
class AppConfig:
    """
    Aggregate application configuration.
    """
    app_info: AppInfo
    db_settings: DatabaseSettings
    theme: Theme


def provide_app_config(
    app_info: AppInfo | None = None,
    db_settings: DatabaseSettings | None = None,
    theme: Theme | None = None,
) -> AppConfig:
    """
    Build and return the full application configuration.
    Optional arguments allow overriding defaults, which
    is useful for testing or custom environments.
    """
    return AppConfig(
        app_info=app_info or provide_app_settings(),
        db_settings=db_settings or load_db_settings(),
        theme=theme or provide_theme_settings(),
    )


__all__ = [
    "AppConfig",
    "provide_app_config",
]