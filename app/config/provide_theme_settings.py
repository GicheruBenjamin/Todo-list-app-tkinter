# app/config/provide_theme_settings.py
from app.types import Theme, FontWeight

def provide_theme_settings() -> Theme:
    return Theme(
        theme_name="Light",
        primary_color="#3860ff",
        bg_color="#ffffff",
        text_color="#000000",
        bordercolor="#cccccc",
        hover_color="#f0f0f0",
        font_family="Arial",
        font_size=12,
        font_weight=FontWeight.NORMAL
    )
