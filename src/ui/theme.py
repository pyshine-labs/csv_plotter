"""
Theme management for the application.
"""
from PyQt5.QtWidgets import QApplication
from ..utils.constants import LIGHT_STYLE, DARK_STYLE


class ThemeManager:
    """Manages UI theme switching."""

    LIGHT = 'light'
    DARK = 'dark'

    _current_theme = LIGHT

    @classmethod
    def current_theme(cls) -> str:
        return cls._current_theme

    @classmethod
    def apply_theme(cls, theme: str) -> None:
        """Apply a theme to the whole application."""
        if theme == cls.LIGHT:
            stylesheet = LIGHT_STYLE
        elif theme == cls.DARK:
            stylesheet = DARK_STYLE
        else:
            raise ValueError(f'Unknown theme: {theme}')

        app = QApplication.instance()
        if app:
            app.setStyleSheet(stylesheet)
            cls._current_theme = theme

    @classmethod
    def toggle_theme(cls) -> str:
        """Switch between light and dark themes."""
        new_theme = cls.DARK if cls._current_theme == cls.LIGHT else cls.LIGHT
        cls.apply_theme(new_theme)
        return new_theme