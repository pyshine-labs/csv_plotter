"""
Unit tests for CSV parser.
"""
import tempfile
import pandas as pd
import pytest
from src.model.csv_parser import CSVParser


@pytest.fixture
def parser():
    return CSVParser()


def test_load_valid_csv_with_header(parser):
    """Test loading a standard CSV with headers."""
    content = """X,Y,Category
1.0,2.5,A
2.0,3.7,B
3.0,5.2,A
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (3, 3)
        assert list(df.columns) == ['X', 'Y', 'Category']
        assert df['X'].dtype in (float, int)
        assert df['Y'].dtype in (float, int)
    finally:
        import os
        os.unlink(fname)


def test_load_csv_semicolon_delimiter(parser):
    """Test CSV with semicolon delimiter."""
    content = """X;Y;Category
1.0;2.5;A
2.0;3.7;B
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert df.shape == (2, 3)
        assert list(df.columns) == ['X', 'Y', 'Category']
    finally:
        import os
        os.unlink(fname)


def test_load_csv_tab_delimiter(parser):
    """Test CSV with tab delimiter."""
    content = """X\tY\tCategory
1.0\t2.5\tA
2.0\t3.7\tB
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert df.shape == (2, 3)
        assert list(df.columns) == ['X', 'Y', 'Category']
    finally:
        import os
        os.unlink(fname)


def test_load_csv_no_header(parser):
    """Test CSV without header; parser should assign default column names."""
    content = """1.0,2.5,A
2.0,3.7,B
3.0,5.2,C
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert df.shape == (3, 3)
        assert df.columns[0] == 'Column_0'
        assert df.columns[1] == 'Column_1'
        assert df.columns[2] == 'Column_2'
    finally:
        import os
        os.unlink(fname)


def test_load_csv_encoding_utf8(parser):
    """Test UTF‑8 encoded CSV with special characters."""
    content = """X,Y,Description
1,2, café
3,4, naïve
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', encoding='utf-8', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert df.shape == (2, 3)
        assert df['Description'].iloc[0] == ' café'
    finally:
        import os
        os.unlink(fname)


def test_load_csv_encoding_latin1(parser):
    """Test Latin‑1 encoded CSV (common Windows)."""
    content = """X,Y,Text
1,2, café
3,4, naïve
"""
    # Encode as latin‑1 (some characters may not be representable, but we'll try)
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.csv', delete=False) as f:
        f.write(content.encode('latin-1'))
        fname = f.name
    try:
        df = parser.load(fname)
        # Should load without UnicodeDecodeError
        assert df.shape == (2, 3)
    finally:
        import os
        os.unlink(fname)


def test_load_empty_csv_raises(parser):
    """Loading an empty CSV should raise pd.errors.EmptyDataError."""
    content = ""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        with pytest.raises(pd.errors.EmptyDataError):
            parser.load(fname)
    finally:
        import os
        os.unlink(fname)


def test_load_malformed_csv_falls_back(parser):
    """Malformed CSV should trigger fallback parsing or raise ValueError."""
    # Create a file that is not CSV at all
    content = "This is not a CSV file\nRandom text\n"
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        # If we get here, fallback succeeded; we should have a DataFrame
        assert isinstance(df, pd.DataFrame)
    except ValueError:
        # Expected if parsing fails completely
        pass
    finally:
        import os
        os.unlink(fname)


def test_numeric_conversion(parser):
    """Ensure numeric columns are converted to numeric dtypes."""
    content = """A,B,C
1,2.5,foo
3,4.7,bar
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        assert pd.api.types.is_numeric_dtype(df['A'])
        assert pd.api.types.is_numeric_dtype(df['B'])
        assert not pd.api.types.is_numeric_dtype(df['C'])
    finally:
        import os
        os.unlink(fname)


def test_drop_empty_rows_and_columns(parser):
    """Ensure completely empty rows/columns are removed."""
    content = """X,Y,Z
1,2,3
,,
,,
4,5,6
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(content)
        fname = f.name
    try:
        df = parser.load(fname)
        # Should drop the two empty rows (index 1 and 2)
        assert df.shape == (2, 3)  # rows 0 and 3 remain
    finally:
        import os
        os.unlink(fname)


def test_max_rows_preview(parser):
    """Ensure parser respects max_rows_preview (limited to 1000 rows)."""
    # Create CSV with 2000 rows
    import csv
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['X', 'Y'])
        for i in range(2000):
            writer.writerow([i, i*2])
        fname = f.name
    try:
        df = parser.load(fname)
        # The parser limits to max_rows_preview = 1000
        assert len(df) == 1000
    finally:
        import os
        os.unlink(fname)