"""
Application-wide constants.
"""

APP_NAME = 'CSV Drag‑and‑Drop Plotter'
VERSION = '1.0.0'
SUPPORTED_FORMATS = ('.csv', '.txt')
MAX_FILE_SIZE_MB = 100  # limit for CSV loading
DEFAULT_PLOT_TYPE = 'scatter'
PLOT_TYPES = ['scatter', 'line', 'bar', 'histogram', 'box']

# UI Colors (for themes)
COLOR_PRIMARY = '#0078d7'
COLOR_SECONDARY = '#6c757d'
COLOR_SUCCESS = '#28a745'
COLOR_DANGER = '#dc3545'
COLOR_WARNING = '#ffc107'
COLOR_INFO = '#17a2b8'

# Style sheet strings
LIGHT_STYLE = """
QMainWindow {
    background-color: #f8f9fa;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}
QTableView {
    color: #000000;
    background-color: #ffffff;
    alternate-background-color: #f0f0f0;
    gridline-color: #cccccc;
}
"""

DARK_STYLE = """
QMainWindow {
    background-color: #2b2b2b;
    color: #ddd;
}
QGroupBox {
    font-weight: bold;
    border: 1px solid #555;
    border-radius: 5px;
    margin-top: 10px;
    padding-top: 10px;
    color: #ddd;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: #aaa;
}
QTableView {
    color: #000000;
    background-color: #ffffff;
    alternate-background-color: #f0f0f0;
    gridline-color: #cccccc;
}
"""