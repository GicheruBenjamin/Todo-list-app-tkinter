# app/config/provide_app_settings.py
"""
Provide app settings.
"""
from app.types import Appinfo

def provide_app_settings() -> Appinfo:
    """
    Provide app settings.
    """
    return Appinfo(
        app_name = "Todoie",
        version = "0.1.0",
        author = "Gicheru Benjamin",
        window_title = "Todoie",
        description = "A simple todo list app",
        window_size = (800, 600),
        icon_path = "/assets/icons/main.png"
    )
