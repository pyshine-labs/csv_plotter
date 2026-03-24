"""
Unit tests for DataModel.
"""
import pandas as pd
import numpy as np
import pytest
from src.model.data_model import DataModel


@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame with mixed numeric and non‑numeric columns."""
    data = {
        'A': [1, 2, 3, 4, 5],
        'B': [1.5, 2.5, 3.5, 4.5, 5.5],
        'C': ['foo', 'bar', 'baz', 'qux', 'quux'],
        'D': [10, 20, 30, 40, 50],
    }
    return pd.DataFrame(data)


@pytest.fixture
def data_model(sample_dataframe):
    return DataModel(sample_dataframe)


def test_data_model_initialization(data_model, sample_dataframe):
    """Test that DataModel wraps the DataFrame correctly."""
    assert data_model.dataframe.equals(sample_dataframe)
    assert data_model.shape() == sample_dataframe.shape


def test_columns(data_model):
    """Test columns property."""
    assert data_model.columns() == ['A', 'B', 'C', 'D']


def test_numeric_columns(data_model):
    """Test numeric_columns property."""
    # Columns A, B, D are numeric; C is object
    numeric = data_model.numeric_columns()
    assert 'A' in numeric
    assert 'B' in numeric
    assert 'D' in numeric
    assert 'C' not in numeric
    assert len(numeric) == 3


def test_get_column_existing(data_model):
    """Test retrieving an existing column."""
    col = data_model.get_column('A')
    assert isinstance(col, pd.Series)
    assert col.tolist() == [1, 2, 3, 4, 5]


def test_get_column_nonexistent(data_model):
    """Test retrieving a non‑existent column returns None."""
    assert data_model.get_column('Missing') is None


def test_get_column_data_existing(data_model):
    """Test retrieving column data as numpy array."""
    arr = data_model.get_column_data('B')
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == np.float64
    np.testing.assert_array_almost_equal(arr, [1.5, 2.5, 3.5, 4.5, 5.5])


def test_get_column_data_nonexistent(data_model):
    """Test retrieving column data for missing column returns None."""
    assert data_model.get_column_data('Missing') is None


def test_get_summary(data_model):
    """Test summary statistics."""
    summary = data_model.get_summary()
    assert isinstance(summary, dict)
    # Should contain statistics for numeric columns
    assert 'A' in summary
    assert 'B' in summary
    assert 'D' in summary
    # Non‑numeric column may be omitted or have different stats
    # depending on pandas describe(include='all')
    # We'll just check that we got something
    assert len(summary) >= 3


def test_head(data_model):
    """Test head method."""
    head_df = data_model.head(2)
    assert isinstance(head_df, pd.DataFrame)
    assert len(head_df) == 2
    assert head_df['A'].tolist() == [1, 2]


def test_tail(data_model):
    """Test tail method."""
    tail_df = data_model.tail(2)
    assert len(tail_df) == 2
    assert tail_df['A'].tolist() == [4, 5]


def test_data_model_with_empty_dataframe():
    """Test DataModel with an empty DataFrame."""
    empty_df = pd.DataFrame()
    model = DataModel(empty_df)
    assert model.columns() == []
    assert model.numeric_columns() == []
    assert model.shape() == (0, 0)
    assert model.get_column('any') is None
    assert model.get_column_data('any') is None
    summary = model.get_summary()
    # Empty dict or with some structure? pandas describe returns empty DataFrame
    # We'll accept whatever.
    assert isinstance(summary, dict)


def test_data_model_with_all_nonnumeric():
    """Test DataModel with no numeric columns."""
    df = pd.DataFrame({
        'Text': ['a', 'b', 'c'],
        'Category': ['x', 'y', 'z']
    })
    model = DataModel(df)
    assert model.numeric_columns() == []
    assert model.get_column_data('Text') is not None  # but will be object array


def test_data_model_immutability(data_model):
    """Ensure the internal DataFrame is not accidentally mutated."""
    df = data_model.dataframe
    # Modify the returned copy should not affect internal data
    df['A'] = [99, 99, 99, 99, 99]
    assert data_model.dataframe['A'].tolist() == [1, 2, 3, 4, 5]