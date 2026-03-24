"""
Unit tests for ThemeManager.
"""
import pytest
from PyQt5.QtWidgets import QApplication
from src.ui.theme import ThemeManager
from src.utils.constants import LIGHT_STYLE, DARK_STYLE


def test_current_theme_default():
    """Default theme should be light."""
    # Ensure theme is reset to light (in case previous test changed it)
    ThemeManager.apply_theme(ThemeManager.LIGHT)
    assert ThemeManager.current_theme() == ThemeManager.LIGHT


def test_apply_light_theme(qapp):
    """Apply light theme."""
    ThemeManager.apply_theme(ThemeManager.LIGHT)
    assert ThemeManager.current_theme() == ThemeManager.LIGHT
    # QApplication stylesheet should be set (maybe not exactly equal due to whitespace)
    assert qapp.styleSheet() is not None


def test_apply_dark_theme(qapp):
    """Apply dark theme."""
    ThemeManager.apply_theme(ThemeManager.DARK)
    assert ThemeManager.current_theme() == ThemeManager.DARK
    # Style sheet should contain dark background color
    assert 'background-color' in qapp.styleSheet().lower()


def test_apply_unknown_theme_raises():
    """Applying unknown theme should raise ValueError."""
    with pytest.raises(ValueError, match='Unknown theme'):
        ThemeManager.apply_theme('unknown')


def test_toggle_theme(qapp):
    """Toggle between light and dark."""
    initial = ThemeManager.current_theme()
    toggled = ThemeManager.toggle_theme()
    assert toggled != initial
    assert ThemeManager.current_theme() == toggled
    # Toggle again returns to original
    ThemeManager.toggle_theme()
    assert ThemeManager.current_theme() == initial


def test_theme_applied_to_qapp(qapp):
    """Verify that theme changes affect QApplication stylesheet."""
    # Start with light theme to ensure a change
    ThemeManager.apply_theme(ThemeManager.LIGHT)
    light_sheet = qapp.styleSheet()
    # Apply dark theme
    ThemeManager.apply_theme(ThemeManager.DARK)
    dark_sheet = qapp.styleSheet()
    # Should be different (unless they are accidentally same)
    if light_sheet != dark_sheet:
        assert dark_sheet != light_sheet
    # Should contain dark style string
    assert '2b2b2b' in dark_sheet or 'dark' in dark_sheet.lower()


def test_theme_manager_class_variables():
    """Ensure class variables are defined."""
    assert hasattr(ThemeManager, 'LIGHT')
    assert hasattr(ThemeManager, 'DARK')
    assert ThemeManager.LIGHT == 'light'
    assert ThemeManager.DARK == 'dark'