# app/config/provide_app_settings.py
"""
Provide app settings.
"""

from pathlib import Path
from app.types import AppInfo

def provide_app_settings() -> AppInfo:
    return AppInfo(
        app_name="Todoie",
        version="0.1.0",
        author="Gicheru Benjamin",
        window_title="Todoie",
        description="A simple todo list app",
        window_size=(800, 600),
        icon_path=Path("assets/icons/main.png")  # now Path instead of str
    )
