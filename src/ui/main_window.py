"""
Main window for CSV Drag‑and‑Drop Plotting application.
"""
import sys
import traceback
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTableView, QToolBar, QStatusBar, QMessageBox, QFileDialog,
    QApplication, QLabel
)
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPalette

from ..model.data_model import DataModel
from ..model.csv_parser import CSVParser
from ..model.table_model import PandasTableModel
from .drop_area import DropArea
from .control_panel import ControlPanel
from ..plot.plot_canvas import PlotCanvas
from ..plot.plot_controller import PlotController
from ..utils.constants import APP_NAME, SUPPORTED_FORMATS


class MainWindow(QMainWindow):
    """Main application window."""

    # Signal emitted when a CSV file is loaded successfully
    data_loaded = pyqtSignal()

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setWindowTitle(APP_NAME)
        self.setGeometry(100, 100, 1200, 800)  # x, y, width, height

        # Core components
        self.data_model: Optional[DataModel] = None
        self.csv_parser = CSVParser()
        self.table_model: Optional[PandasTableModel] = None
        self.plot_controller: Optional[PlotController] = None

        # UI widgets
        self.drop_area: Optional[DropArea] = None
        self.table_view: Optional[QTableView] = None
        self.control_panel: Optional[ControlPanel] = None
        self.plot_canvas: Optional[PlotCanvas] = None

        self._init_ui()
        self._connect_signals()
        self._update_ui_state(has_data=False)

    def _init_ui(self) -> None:
        """Initialize all UI components and layout."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # --- Top section: Drop area + Table + Control panel ---
        top_splitter = QSplitter(Qt.Horizontal)

        # Left side: drop area and table view stacked vertically
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        # Drop area
        self.drop_area = DropArea()
        left_layout.addWidget(self.drop_area, 1)  # stretch

        # Table view
        self.table_view = QTableView()
        self.table_view.setAlternatingRowColors(True)
        self.table_view.setSortingEnabled(True)
        # Ensure text color is black
        palette = self.table_view.palette()
        palette.setColor(palette.Text, Qt.black)
        self.table_view.setPalette(palette)
        left_layout.addWidget(self.table_view, 2)

        top_splitter.addWidget(left_widget)

        # Right side: control panel
        self.control_panel = ControlPanel()
        top_splitter.addWidget(self.control_panel)

        # Set initial splitter sizes (2:1 ratio)
        top_splitter.setSizes([800, 400])

        main_layout.addWidget(top_splitter, 4)  # 4/5 of height

        # --- Bottom section: Matplotlib canvas ---
        self.plot_canvas = PlotCanvas()
        main_layout.addWidget(self.plot_canvas, 6)  # 6/10? Actually we want canvas larger

        # Create menu bar and toolbar
        self._create_menu_bar()
        self._create_toolbar()

        # Status bar
        self.statusBar().showMessage('Ready. Drag and drop a CSV file to begin.')

    def _create_menu_bar(self) -> None:
        """Create the application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu('&File')
        open_action = file_menu.addAction('&Open...', self._on_open_file,
                                          shortcut='Ctrl+O')
        file_menu.addSeparator()
        save_plot_action = file_menu.addAction('&Save Plot...', self._on_save_plot,
                                               shortcut='Ctrl+S')
        file_menu.addSeparator()
        exit_action = file_menu.addAction('E&xit', self.close,
                                          shortcut='Ctrl+Q')

        # View menu
        view_menu = menubar.addMenu('&View')
        view_menu.addAction('&Toggle Table', self._toggle_table)
        view_menu.addAction('&Toggle Controls', self._toggle_controls)
        view_menu.addSeparator()
        view_menu.addAction('&Light Theme', lambda: self._set_theme('light'))
        view_menu.addAction('&Dark Theme', lambda: self._set_theme('dark'))

        # Help menu
        help_menu = menubar.addMenu('&Help')
        help_menu.addAction('&About', self._show_about)
        help_menu.addAction('&Documentation', self._show_documentation)

    def _create_toolbar(self) -> None:
        """Create a toolbar with common actions."""
        toolbar = QToolBar('Main Toolbar')
        self.addToolBar(toolbar)

        toolbar.addAction('Open', self._on_open_file)
        toolbar.addAction('Save Plot', self._on_save_plot)
        toolbar.addSeparator()
        toolbar.addAction('Zoom In', self.plot_canvas.zoom_in)
        toolbar.addAction('Zoom Out', self.plot_canvas.zoom_out)
        toolbar.addAction('Home', self.plot_canvas.home)
        toolbar.addSeparator()
        toolbar.addAction('Light', lambda: self._set_theme('light'))
        toolbar.addAction('Dark', lambda: self._set_theme('dark'))

    def _connect_signals(self) -> None:
        """Connect signals between components."""
        # Drop area -> load CSV
        if self.drop_area:
            self.drop_area.file_dropped.connect(self._load_csv_file)

        # Control panel -> plot updates
        if self.control_panel:
            self.control_panel.plot_requested.connect(self._update_plot)

        # Data loaded signal
        self.data_loaded.connect(self._on_data_loaded)

    def _update_ui_state(self, has_data: bool) -> None:
        """Enable/disable UI elements based on whether data is loaded."""
        if self.control_panel:
            self.control_panel.setEnabled(has_data)
        if self.plot_canvas:
            self.plot_canvas.setEnabled(has_data)
        # TODO: disable save plot if no plot

    # ---------- Slot implementations ----------

    def _load_csv_file(self, file_path: str) -> None:
        """Load a CSV file from the given path."""
        try:
            # Parse CSV
            dataframe = self.csv_parser.load(file_path)
            # Create data model
            self.data_model = DataModel(dataframe)
            # Update table model
            self.table_model = PandasTableModel(dataframe)
            self.table_view.setModel(self.table_model)
            # Update control panel column lists
            if self.control_panel:
                self.control_panel.set_columns(self.data_model.columns())
            # Create plot controller
            self.plot_controller = PlotController(self.data_model, self.plot_canvas)
            # Update UI
            self._update_ui_state(has_data=True)
            self.statusBar().showMessage(f'Loaded {file_path}', 5000)
            self.data_loaded.emit()
        except Exception as e:
            QMessageBox.critical(self, 'Error Loading CSV',
                                 f'Could not load CSV file:\n{str(e)}\n\n{traceback.format_exc()}')
            self.statusBar().showMessage('Failed to load CSV', 5000)

    def _on_open_file(self) -> None:
        """Open file dialog to select a CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Open CSV File', '',
            f'CSV Files (*.csv *.txt);;All Files (*.*)'
        )
        if file_path:
            self._load_csv_file(file_path)

    def _on_save_plot(self) -> None:
        """Save the current plot to an image file."""
        if not self.plot_canvas:
            return
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, 'Save Plot', '',
            'PNG (*.png);;JPEG (*.jpg);;PDF (*.pdf);;SVG (*.svg)'
        )
        if file_path:
            self.plot_canvas.save_plot(file_path)

    def _update_plot(self) -> None:
        """Generate plot based on current selections."""
        if not self.plot_controller or not self.control_panel:
            return
        try:
            x_col = self.control_panel.x_column()
            y_col = self.control_panel.y_column()
            plot_type = self.control_panel.plot_type()
            options = self.control_panel.options()
            self.plot_controller.generate_plot(x_col, y_col, plot_type, options)
            self.statusBar().showMessage('Plot updated', 3000)
        except Exception as e:
            QMessageBox.warning(self, 'Plot Error',
                                f'Could not generate plot:\n{str(e)}')

    def _on_data_loaded(self) -> None:
        """Called after data is loaded; auto‑plot if possible."""
        if self.control_panel and self.data_model:
            # Try to auto‑select first two numeric columns
            numeric_cols = self.data_model.numeric_columns()
            if len(numeric_cols) >= 2:
                self.control_panel.set_selection(numeric_cols[0], numeric_cols[1], 'scatter')
                self._update_plot()

    def _toggle_table(self) -> None:
        """Show/hide the table view."""
        if self.table_view:
            self.table_view.setVisible(not self.table_view.isVisible())

    def _toggle_controls(self) -> None:
        """Show/hide the control panel."""
        if self.control_panel:
            self.control_panel.setVisible(not self.control_panel.isVisible())

    def _set_theme(self, theme: str) -> None:
        """Switch UI theme (light/dark)."""
        # TODO: integrate ThemeManager
        from ..ui.theme import ThemeManager
        ThemeManager.apply_theme(theme)
        self.statusBar().showMessage(f'Switched to {theme} theme', 3000)

    def _show_about(self) -> None:
        """Show about dialog."""
        QMessageBox.about(self, f'About {APP_NAME}',
                          'CSV Drag‑and‑Drop Plotting Application\n\n'
                          'Version 1.0.0\n'
                          'Built with PyQt5, matplotlib, and pandas.')

    def _show_documentation(self) -> None:
        """Open documentation in browser."""
        # TODO: implement
        QMessageBox.information(self, 'Documentation',
                                'Documentation is available in the docs/ folder.')


def main() -> None:
    """Application entry point."""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # modern look
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()