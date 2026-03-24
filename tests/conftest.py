"""
Pytest fixtures for CSV Plotter tests.
"""
import pytest
from PyQt5.QtWidgets import QApplication


@pytest.fixture(scope="session")
def qapp():
    """Provide a single QApplication instance for the entire test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Do not quit the app; let pytest-qt handle cleanup.


@pytest.fixture
def qtbot(qapp, request):
    """Provide a QtBot instance for widget testing.
    
    This fixture is provided by pytest-qt, but we need to ensure QApplication exists.
    """
    from pytestqt.qtbot import QtBot
    bot = QtBot(request)
    yield bot
    bot.wait(50)