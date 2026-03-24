"""
Control panel for selecting plot parameters.
"""
from typing import List, Optional

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QLabel, QComboBox, QPushButton, QCheckBox,
    QFormLayout, QSpinBox, QDoubleSpinBox
)


class ControlPanel(QWidget):
    """Right‑side panel with plot controls."""

    # Signal emitted when user requests a plot update
    plot_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns: List[str] = []
        self._init_ui()
        self._connect_internal()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # --- Column selection group ---
        col_group = QGroupBox('Data Columns')
        col_form = QFormLayout(col_group)

        self.x_combo = QComboBox()
        self.x_combo.setToolTip('Select column for X axis')
        col_form.addRow('X axis:', self.x_combo)

        self.y_combo = QComboBox()
        self.y_combo.setToolTip('Select column for Y axis')
        col_form.addRow('Y axis:', self.y_combo)

        layout.addWidget(col_group)

        # --- Plot type group ---
        type_group = QGroupBox('Plot Type')
        type_layout = QVBoxLayout(type_group)
        self.plot_type_combo = QComboBox()
        self.plot_type_combo.addItems(['Scatter', 'Line', 'Bar', 'Histogram', 'Box'])
        self.plot_type_combo.setCurrentIndex(0)
        type_layout.addWidget(self.plot_type_combo)
        layout.addWidget(type_group)

        # --- Options group ---
        opts_group = QGroupBox('Options')
        opts_layout = QVBoxLayout(opts_group)
        self.grid_check = QCheckBox('Show grid')
        self.grid_check.setChecked(True)
        opts_layout.addWidget(self.grid_check)

        self.legend_check = QCheckBox('Show legend')
        self.legend_check.setChecked(False)
        opts_layout.addWidget(self.legend_check)

        # Axis labels
        label_layout = QFormLayout()
        self.x_label_edit = QComboBox()
        self.x_label_edit.setEditable(True)
        self.x_label_edit.setToolTip('Label for X axis')
        label_layout.addRow('X label:', self.x_label_edit)
        self.y_label_edit = QComboBox()
        self.y_label_edit.setEditable(True)
        self.y_label_edit.setToolTip('Label for Y axis')
        label_layout.addRow('Y label:', self.y_label_edit)
        opts_layout.addLayout(label_layout)

        # Plot title
        self.title_edit = QComboBox()
        self.title_edit.setEditable(True)
        self.title_edit.setToolTip('Title of the plot')
        opts_layout.addWidget(QLabel('Title:'))
        opts_layout.addWidget(self.title_edit)

        layout.addWidget(opts_group)

        # --- Update button ---
        self.update_button = QPushButton('Update Plot')
        self.update_button.setStyleSheet(
            'QPushButton { padding: 8px; font-weight: bold; }'
        )
        layout.addWidget(self.update_button)

        layout.addStretch()

    def _connect_internal(self):
        """Connect internal signals."""
        self.update_button.clicked.connect(self.plot_requested.emit)
        # Optionally auto‑update when selection changes
        self.x_combo.currentTextChanged.connect(self._on_selection_changed)
        self.y_combo.currentTextChanged.connect(self._on_selection_changed)
        self.plot_type_combo.currentTextChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        """Emit plot request if auto‑update is enabled."""
        # In the future we could have an auto‑update checkbox
        pass

    # ---------- Public API ----------

    def set_columns(self, columns: List[str]) -> None:
        """Populate the column selection combos with the given list."""
        self._columns = columns.copy()
        self.x_combo.clear()
        self.y_combo.clear()
        self.x_combo.addItems(columns)
        self.y_combo.addItems(columns)
        # Auto‑select first two columns if possible
        if len(columns) >= 1:
            self.x_combo.setCurrentIndex(0)
        else:
            self.x_combo.setCurrentIndex(-1)
        if len(columns) >= 2:
            self.y_combo.setCurrentIndex(1)
        else:
            self.y_combo.setCurrentIndex(-1)
        # Also populate label suggestions
        self.x_label_edit.clear()
        self.y_label_edit.clear()
        self.x_label_edit.addItems(columns)
        self.y_label_edit.addItems(columns)
        self.title_edit.clear()
        self.title_edit.addItems([f'Plot of {columns[0]} vs {columns[1]}' if len(columns) >= 2 else ''])

    def set_selection(self, x_col: str, y_col: str, plot_type: str) -> None:
        """Set the current selection programmatically."""
        idx_x = self.x_combo.findText(x_col)
        if idx_x >= 0:
            self.x_combo.setCurrentIndex(idx_x)
        idx_y = self.y_combo.findText(y_col)
        if idx_y >= 0:
            self.y_combo.setCurrentIndex(idx_y)
        idx_type = self.plot_type_combo.findText(plot_type, Qt.MatchFixedString)
        if idx_type >= 0:
            self.plot_type_combo.setCurrentIndex(idx_type)

    def x_column(self) -> Optional[str]:
        """Return the currently selected X column."""
        return self.x_combo.currentText() if self.x_combo.currentIndex() >= 0 else None

    def y_column(self) -> Optional[str]:
        """Return the currently selected Y column."""
        return self.y_combo.currentText() if self.y_combo.currentIndex() >= 0 else None

    def plot_type(self) -> str:
        """Return the selected plot type."""
        return self.plot_type_combo.currentText().lower()

    def options(self) -> dict:
        """Return a dictionary of plot options."""
        return {
            'grid': self.grid_check.isChecked(),
            'legend': self.legend_check.isChecked(),
            'x_label': self.x_label_edit.currentText(),
            'y_label': self.y_label_edit.currentText(),
            'title': self.title_edit.currentText(),
        }