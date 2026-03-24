"""
Data model that holds the loaded CSV data as a pandas DataFrame.
"""
from typing import List, Optional, Union
import pandas as pd
import numpy as np


class DataModel:
    """Wrapper around a pandas DataFrame with convenience methods."""

    def __init__(self, dataframe: pd.DataFrame):
        self._df = dataframe.copy()
        self._numeric_columns = self._compute_numeric_columns()

    def _compute_numeric_columns(self) -> List[str]:
        """Return column names that have numeric dtype."""
        numeric_cols = []
        for col in self._df.columns:
            if pd.api.types.is_numeric_dtype(self._df[col]):
                numeric_cols.append(col)
        return numeric_cols

    @property
    def dataframe(self) -> pd.DataFrame:
        """Return the underlying DataFrame (read‑only)."""
        return self._df.copy()

    def columns(self) -> List[str]:
        """Return all column names."""
        return list(self._df.columns)

    def numeric_columns(self) -> List[str]:
        """Return column names that contain numeric data."""
        return self._numeric_columns.copy()

    def get_column(self, column_name: str) -> Optional[pd.Series]:
        """Return a column as a pandas Series, or None if column does not exist."""
        if column_name in self._df.columns:
            return self._df[column_name]
        return None

    def get_column_data(self, column_name: str) -> Optional[np.ndarray]:
        """Return column values as a numpy array, or None."""
        col = self.get_column(column_name)
        if col is not None:
            return col.to_numpy()
        return None

    def get_summary(self) -> dict:
        """Return a dictionary with basic statistics for numeric columns."""
        try:
            desc = self._df.describe(include='all')
            return desc.to_dict()
        except ValueError:
            # Empty DataFrame or no columns
            return {}

    def shape(self) -> tuple:
        """Return (rows, columns) of the DataFrame."""
        return self._df.shape

    def head(self, n: int = 5) -> pd.DataFrame:
        """Return the first n rows."""
        return self._df.head(n)

    def tail(self, n: int = 5) -> pd.DataFrame:
        """Return the last n rows."""
        return self._df.tail(n)