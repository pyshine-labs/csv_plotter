"""
CSV parsing with automatic delimiter detection and error handling.
"""
import pandas as pd
import chardet
from typing import Optional, Tuple
import traceback
from pandas.errors import EmptyDataError


class CSVParser:
    """Load CSV files into pandas DataFrames with robust detection."""

    def __init__(self):
        # Configuration
        self.default_encoding = 'utf-8'
        self.max_rows_preview = 1000  # limit for large files
        self.supported_delimiters = [',', ';', '\t', '|', ' ']

    def load(self, file_path: str) -> pd.DataFrame:
        """
        Load a CSV file, trying to guess delimiter, encoding, and header.

        Raises:
            ValueError: if the file cannot be parsed as CSV.
            FileNotFoundError: if the file does not exist.
            pd.errors.EmptyDataError: if the file is empty.
        """
        # Determine pandas version for compatibility
        pd_version = tuple(map(int, pd.__version__.split('.')[:2]))
        
        # Encodings to try in order of preference
        detected_encoding = self._detect_encoding(file_path)
        encodings_to_try = [
            detected_encoding,
            'latin-1',
            'cp1252',
            'ISO-8859-1',
            'utf-8-sig',
            'utf-8'
        ]
        # Deduplicate while preserving order
        seen = set()
        unique_encodings = []
        for enc in encodings_to_try:
            if enc not in seen:
                seen.add(enc)
                unique_encodings.append(enc)
        
        # Keep track of the last error to raise if all attempts fail
        last_error = None
        
        for encoding in unique_encodings:
            try:
                delimiter, has_header = self._guess_dialect(file_path, encoding)
                # Primary attempt with strict error handling
                read_csv_kwargs = {
                    'filepath_or_buffer': file_path,
                    'delimiter': delimiter,
                    'encoding': encoding,
                    'header': 'infer' if has_header else None,
                    'skip_blank_lines': True,
                    'low_memory': False,
                    'nrows': self.max_rows_preview
                }
                if pd_version >= (1, 3):
                    read_csv_kwargs['on_bad_lines'] = 'warn'
                else:
                    read_csv_kwargs['error_bad_lines'] = False
                    read_csv_kwargs['warn_bad_lines'] = True
                df = pd.read_csv(**read_csv_kwargs)
            except UnicodeDecodeError:
                # This encoding cannot decode the file, try next
                continue
            except Exception as e:
                # If the file is empty, re‑raise EmptyDataError
                if isinstance(e, EmptyDataError):
                    raise
                # For other errors, try fallback reading with same encoding
                try:
                    fallback_kwargs = {'filepath_or_buffer': file_path, 'encoding': encoding}
                    if pd_version >= (1, 3):
                        fallback_kwargs['on_bad_lines'] = 'skip'
                    else:
                        fallback_kwargs['error_bad_lines'] = False
                    df = pd.read_csv(**fallback_kwargs)
                except Exception as e2:
                    if isinstance(e2, EmptyDataError):
                        raise
                    # Store error and continue to next encoding
                    last_error = e2
                    continue
            # If we reach here, reading succeeded
            # Clean up column names if no header
            if not has_header:
                df.columns = [f'Column_{i}' for i in range(df.shape[1])]

            # Drop completely empty rows/columns
            df.dropna(how='all', inplace=True)
            df.dropna(axis=1, how='all', inplace=True)

            # Reset index
            df.reset_index(drop=True, inplace=True)

            # Convert numeric columns where possible
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except (ValueError, TypeError):
                    # column cannot be converted to numeric; leave as is
                    pass

            return df
        
        # All encodings exhausted
        raise ValueError(
            f'Failed to parse CSV with any encoding. Last error: {last_error}'
        )

    def _detect_encoding(self, file_path: str) -> str:
        """Detect file encoding using chardet."""
        try:
            with open(file_path, 'rb') as f:
                raw = f.read(10000)  # sample first 10 kB
            result = chardet.detect(raw)
            encoding = result['encoding'] if result['confidence'] > 0.7 else self.default_encoding
            # Fallback to utf‑8 if encoding is None
            if encoding is None:
                encoding = self.default_encoding
            return encoding
        except Exception:
            return self.default_encoding

    def _guess_dialect(self, file_path: str, encoding: str) -> Tuple[str, bool]:
        """
        Guess CSV delimiter and whether a header is present.

        Returns:
            delimiter (str), has_header (bool)
        """
        # Read first few lines
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                lines = [f.readline() for _ in range(5)]
        except UnicodeDecodeError:
            # fallback to latin‑1
            with open(file_path, 'r', encoding='latin-1') as f:
                lines = [f.readline() for _ in range(5)]

        # Remove empty lines
        lines = [line.strip() for line in lines if line.strip()]

        if not lines:
            return ',', True  # default

        # Count occurrences of candidate delimiters
        delimiter_counts = {}
        for delim in self.supported_delimiters:
            count = sum(line.count(delim) for line in lines)
            delimiter_counts[delim] = count

        # Choose delimiter with highest count, but at least one occurrence
        best_delim = ','
        best_count = 0
        for delim, count in delimiter_counts.items():
            if count > best_count:
                best_delim = delim
                best_count = count

        # If no delimiter found, assume single column (no delimiter)
        if best_count == 0:
            best_delim = ','

        # Guess header: first line contains non‑numeric values?
        first_line = lines[0]
        # Split by best delimiter
        parts = first_line.split(best_delim)
        # If any part looks like a number (integer/float), likely no header
        numeric_parts = 0
        for part in parts:
            part = part.strip()
            if part.replace('.', '', 1).replace('-', '', 1).isdigit():
                numeric_parts += 1
        has_header = numeric_parts / max(len(parts), 1) < 0.5

        return best_delim, has_header