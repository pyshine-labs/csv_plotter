"""
Embedded matplotlib canvas with interactive toolbar.
"""
from typing import Optional, Tuple, List
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np

from PyQt5.QtWidgets import QVBoxLayout, QWidget


class PlotCanvas(QWidget):
    """Widget containing a matplotlib figure and navigation toolbar."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._figure = Figure(figsize=(8, 5), dpi=100)
        self._axes: Axes = self._figure.add_subplot(111)
        self._canvas = FigureCanvasQTAgg(self._figure)
        self._toolbar = NavigationToolbar2QT(self._canvas, self)

        self._init_ui()
        self.clear_plot()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._toolbar)
        layout.addWidget(self._canvas)

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def axes(self) -> Axes:
        return self._axes

    def clear_plot(self):
        """Clear the axes and display a placeholder message."""
        self._axes.clear()
        self._axes.text(0.5, 0.5, 'No plot data.\nLoad a CSV and select columns.',
                        horizontalalignment='center',
                        verticalalignment='center',
                        transform=self._axes.transAxes,
                        fontsize=12, color='gray')
        self._axes.set_xlim(0, 1)
        self._axes.set_ylim(0, 1)
        self._axes.set_xticks([])
        self._axes.set_yticks([])
        self._canvas.draw()

    def draw_plot(self, x_data: np.ndarray, y_data: np.ndarray,
                  plot_type: str = 'scatter', **options):
        """
        Draw a plot on the canvas.

        Parameters:
            x_data: 1D array of X values
            y_data: 1D array of Y values
            plot_type: one of 'scatter', 'line', 'bar', 'histogram', 'box'
            options: additional styling options (grid, labels, title, etc.)
        """
        self._axes.clear()

        if plot_type == 'scatter':
            self._axes.scatter(x_data, y_data, alpha=0.7, edgecolors='k', linewidth=0.5)
        elif plot_type == 'line':
            self._axes.plot(x_data, y_data, marker='o', linestyle='-')
        elif plot_type == 'bar':
            # For bar plots, x_data should be categorical labels
            # We'll use indices if x_data is numeric? Let's treat x_data as positions.
            self._axes.bar(range(len(x_data)), y_data, tick_label=x_data)
        elif plot_type == 'histogram':
            # For histogram, we ignore x_data (maybe bins) and use y_data as values
            self._axes.hist(y_data, bins='auto', edgecolor='black')
        elif plot_type == 'box':
            self._axes.boxplot(y_data)

        # Apply options
        if options.get('grid', True):
            self._axes.grid(True, linestyle='--', alpha=0.5)

        if options.get('x_label'):
            self._axes.set_xlabel(options['x_label'])
        if options.get('y_label'):
            self._axes.set_ylabel(options['y_label'])
        if options.get('title'):
            self._axes.set_title(options['title'])

        if options.get('legend', False):
            self._axes.legend()

        # Auto‑adjust layout
        self._figure.tight_layout()
        self._canvas.draw()

    def save_plot(self, file_path: str):
        """Save the current figure to a file."""
        self._figure.savefig(file_path, dpi=300, bbox_inches='tight')

    # Convenience methods for toolbar actions
    def zoom_in(self):
        """Zoom in (trigger toolbar's zoom)."""
        self._toolbar.zoom()

    def zoom_out(self):
        """Zoom out (trigger toolbar's zoom)."""
        self._toolbar.zoom()

    def home(self):
        """Reset view to original (trigger toolbar's home)."""
        self._toolbar.home()

    def pan(self):
        """Activate pan mode."""
        self._toolbar.pan()