"""
Qt table model for displaying pandas DataFrames.
"""
from typing import Any, Optional
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtGui import QColor


class PandasTableModel(QAbstractTableModel):
    """Adapter between pandas DataFrame and QTableView."""

    def __init__(self, dataframe: pd.DataFrame, parent=None):
        super().__init__(parent)
        self._dataframe = dataframe.copy()
        self._numeric_columns = [
            col for col in self._dataframe.columns
            if pd.api.types.is_numeric_dtype(self._dataframe[col])
        ]

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._dataframe)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._dataframe.columns)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Optional[Any]:
        if not index.isValid():
            return None

        row, col = index.row(), index.column()
        if row >= self.rowCount() or col >= self.columnCount():
            return None

        value = self._dataframe.iat[row, col]

        if role == Qt.DisplayRole:
            # Format numeric values with limited precision
            if pd.isna(value):
                return ''
            if col < len(self._dataframe.columns) and self._dataframe.columns[col] in self._numeric_columns:
                # Format float to 6 significant digits
                return f'{value:.6g}'
            return str(value)

        elif role == Qt.TextAlignmentRole:
            if self._dataframe.columns[col] in self._numeric_columns:
                return Qt.AlignRight | Qt.AlignVCenter
            return Qt.AlignLeft | Qt.AlignVCenter

        elif role == Qt.BackgroundRole:
            # Light gray background for numeric columns
            if self._dataframe.columns[col] in self._numeric_columns:
                return QColor(240, 248, 255)  # alice blue
            # Alternating row colors
            if row % 2 == 0:
                return QColor(250, 250, 250)
        elif role == Qt.ToolTipRole:
            return f'Row {row}, Col {self._dataframe.columns[col]}\nValue: {value}'

        return None

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole) -> Optional[Any]:
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            if section < len(self._dataframe.columns):
                col_name = self._dataframe.columns[section]
                # Add data type hint for numeric columns
                if col_name in self._numeric_columns:
                    dtype = self._dataframe[col_name].dtype
                    return f'{col_name} ({dtype})'
                return col_name
            return ''
        elif orientation == Qt.Vertical:
            return str(section)
        return None

    def sort(self, column: int, order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        """Sort the DataFrame by the given column."""
        if column < 0 or column >= len(self._dataframe.columns):
            return
        col_name = self._dataframe.columns[column]
        ascending = (order == Qt.AscendingOrder)
        self.layoutAboutToBeChanged.emit()
        self._dataframe = self._dataframe.sort_values(
            by=col_name,
            ascending=ascending,
            na_position='last'
        ).reset_index(drop=True)
        self.layoutChanged.emit()

    def dataframe(self) -> pd.DataFrame:
        """Return a copy of the underlying DataFrame."""
        return self._dataframe.copy()