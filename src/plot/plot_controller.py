"""
Controller that orchestrates plot generation.
"""
from typing import Optional
import numpy as np
from ..model.data_model import DataModel
from .plot_canvas import PlotCanvas


class PlotController:
    """Bridges DataModel and PlotCanvas."""

    def __init__(self, data_model: DataModel, plot_canvas: PlotCanvas):
        self._data_model = data_model
        self._plot_canvas = plot_canvas
        self._x_column: Optional[str] = None
        self._y_column: Optional[str] = None
        self._plot_type: str = 'scatter'

    def generate_plot(self, x_column: Optional[str] = None,
                      y_column: Optional[str] = None,
                      plot_type: Optional[str] = None,
                      options: Optional[dict] = None) -> None:
        """
        Generate a plot with the given column selections.

        If columns are None, use previously stored selections.
        """
        if x_column is not None:
            self._x_column = x_column
        if y_column is not None:
            self._y_column = y_column
        if plot_type is not None:
            self._plot_type = plot_type.lower()

        # Validate selections
        if self._x_column is None or self._y_column is None:
            raise ValueError('X and Y columns must be selected.')

        # Retrieve data
        x_data = self._data_model.get_column_data(self._x_column)
        y_data = self._data_model.get_column_data(self._y_column)

        if x_data is None or y_data is None:
            raise ValueError(f'Column(s) not found: {self._x_column}, {self._y_column}')

        # Ensure equal length
        min_len = min(len(x_data), len(y_data))
        if min_len == 0:
            raise ValueError('Selected columns contain no data.')

        x_data = x_data[:min_len]
        y_data = y_data[:min_len]

        # For histogram and box plots, only y_data is used
        if self._plot_type in ('histogram', 'box'):
            # Use y_data only
            pass
        else:
            # Ensure numeric data
            if not (np.issubdtype(x_data.dtype, np.number) and
                    np.issubdtype(y_data.dtype, np.number)):
                raise ValueError('Selected columns must be numeric for this plot type.')

        # Merge options
        default_options = self._build_options()
        if options:
            default_options.update(options)

        # Call canvas to draw
        self._plot_canvas.draw_plot(x_data, y_data, self._plot_type, **default_options)

    def _build_options(self) -> dict:
        """Build a dictionary of plot options (to be extended)."""
        # TODO: read options from UI (control panel)
        return {
            'grid': True,
            'legend': False,
            'x_label': self._x_column,
            'y_label': self._y_column,
            'title': f'{self._plot_type.capitalize()} of {self._y_column} vs {self._x_column}',
        }