# Troubleshooting and FAQ

This document addresses common problems encountered when installing, running, or using the CSV Drag‑and‑Drop Plotter. If your issue is not covered here, please open a GitHub issue with details about your environment and the error messages.

## Installation Issues

### PyQt5 Installation Fails

**Symptoms**: `pip install -r requirements.txt` fails with errors about missing Qt libraries or compilation failures.

**Possible Solutions**:

- **Windows**: Download pre‑built PyQt5 wheels from [PyPI](https://pypi.org/project/PyQt5/) using `pip install PyQt5`. If you have multiple Python versions, ensure you are using the correct pip.
- **macOS**: Use Homebrew to install Qt5: `brew install qt5`, then set environment variable `PYQT5_QT_PLUGIN_PATH`. Alternatively, use `pip install PyQt5`; if it fails, try `pip install pyqt5‑tools`.
- **Linux**: Install system packages first:

  ```bash
  # Debian/Ubuntu
  sudo apt-get install python3-pyqt5
  # Fedora
  sudo dnf install python3-qt5
  # Arch
  sudo pacman -S python-pyqt5
  ```

  Then run `pip install -r requirements.txt` again.

### matplotlib Backend Errors

**Symptoms**: The application starts but the plot canvas is blank, or you see an error about “No module named ‘PyQt5.QtWidgets’”.

**Cause**: matplotlib is using a non‑Qt backend (e.g., TkAgg). The application requires the `Qt5Agg` backend.

**Fix**: Ensure matplotlib is installed after PyQt5. You can force the backend by setting the `MPLBACKEND` environment variable before launching:

```bash
export MPLBACKEND=Qt5Agg   # macOS/Linux
set MPLBACKEND=Qt5Agg      # Windows (Command Prompt)
$env:MPLBACKEND="Qt5Agg"   # Windows (PowerShell)
```

Alternatively, edit your `matplotlibrc` file (see matplotlib documentation).

### Missing Dependencies (pandas, numpy, chardet)

If you see `ModuleNotFoundError` for any of these packages, install them manually:

```bash
pip install pandas numpy chardet
```

## Runtime Issues

### Application Crashes on Launch

**Checklist**:

1. Verify Python version (`python --version`) is 3.7 or higher.
2. Ensure all dependencies are installed (`pip list`).
3. Look for error messages in the terminal. Run the application from a terminal to see the traceback:

   ```bash
   python run.py
   ```

4. If the crash is due to a segmentation fault, it may be a PyQt5 mismatch. Try reinstalling PyQt5:

   ```bash
   pip uninstall PyQt5 PyQt5-sip
   pip install PyQt5
   ```

### CSV File Fails to Load

**Common causes**:

- **File is empty** – The parser raises `EmptyDataError`. Provide a non‑empty CSV.
- **Incorrect delimiter** – The parser tries to detect delimiter automatically, but if the file uses a rare delimiter (e.g., colon), detection may fail. Convert the file to comma‑ or tab‑separated format.
- **Encoding issues** – The parser attempts multiple encodings (UTF‑8, Latin‑1, etc.). If your file uses an unusual encoding (e.g., EBCDIC), convert it to UTF‑8 before loading.
- **Missing header** – The parser assumes the first row is a header. If your file has no header, the parser will treat the first row as data (column names become “Column1”, “Column2”, …). This is usually fine, but if the first row contains numeric data, the column names will be numbers, which may cause confusion.
- **Large file size** – The parser limits preview to 1000 rows for performance. The full dataset is still loaded for plotting, but the table only shows the first 1000 rows. If the file is extremely large (>100 MB), memory usage may be high. Consider sampling the file before loading.

**Debug steps**:

1. Open the CSV in a text editor to verify its format.
2. Try loading the file with pandas directly:

   ```python
   import pandas as pd
   df = pd.read_csv('yourfile.csv')
   ```

   If pandas fails, the CSV is malformed.

3. Check the file extension. The application only accepts `.csv` and `.txt` by default. You can modify `SUPPORTED_FORMATS` in `constants.py` to add other extensions.

### Plot Appears Empty or Incorrect

- **Non‑numeric columns**: The plot functions require numeric data. If you select a column that contains strings or dates, the plot will be empty. Use the data table to verify column types.
- **Missing values (NaN)**: Rows with NaN in the selected columns are silently dropped. This may reduce the number of plotted points.
- **Histogram with inappropriate data**: Histograms require continuous numeric data. If the column contains only a few unique values, the histogram may look odd.
- **Box plot with single group**: Box plots expect multiple groups if the X column is categorical. If you select the same column for X and Y, the plot may be misleading.

**Workaround**: Use the table view to inspect your data, and consider cleaning the CSV before loading.

### UI Looks Blurry or Scaled Incorrectly (High‑DPI Displays)

On Windows and macOS with high‑DPI monitors, Qt may not automatically scale the UI, resulting in tiny or blurry widgets.

**Fix**: Enable Qt’s high‑DPI scaling by setting environment variables before launching:

```bash
export QT_AUTO_SCREEN_SCALE_FACTOR=1   # macOS/Linux
set QT_AUTO_SCREEN_SCALE_FACTOR=1      # Windows
```

Alternatively, adjust the scaling factor manually:

```bash
export QT_SCALE_FACTOR=1.5
```

See the [Qt High‑DPI documentation](https://doc.qt.io/qt-5/highdpi.html) for more options.

### Dark Theme Not Applied Fully

The dark theme stylesheets may not cover every widget, especially custom Qt styles. If some parts remain light, you can extend the theme dictionary in `theme.py`.

## Performance Issues

### Slow Loading of Large CSV Files

The parser reads the entire file into memory. For files larger than 1 GB, this can cause long delays and high memory usage.

**Suggestions**:

- Load a subset of the data (e.g., first 100,000 rows) by editing `max_rows_preview` in `csv_parser.py`.
- Use a more efficient file format (e.g., Parquet, Feather) and extend the parser to support it.
- Increase the `chunksize` in `pd.read_csv` (not currently implemented).

### Slow Plot Updates with Many Points

Plotting hundreds of thousands of points can be slow. Consider:

- Downsampling the data before plotting.
- Using a faster plot type (e.g., line plots are faster than scatter plots with markers).
- Reducing the marker size and disabling anti‑aliasing.

## FAQ

### Q: Can I plot multiple Y columns against the same X column?

**A**: Not in the current version. The UI only supports one X and one Y column at a time. You can work around this by loading the file multiple times or modifying the code to support multiple series (see the Developer Guide).

### Q: Does the application support real‑time data streaming?

**A**: No, it is designed for static CSV files. However, you could extend it to watch a folder for new CSV files and automatically reload.

### Q: Can I change the language of the UI?

**A**: The UI is currently only in English. Internationalization (i18n) could be added by contributing translation files (.ts) and using Qt’s translation system.

### Q: Is there a command‑line interface?

**A**: No, the application is purely graphical. However, you can write a Python script that uses the underlying modules (e.g., `CSVParser`, `PlotCanvas`) to automate plotting.

### Q: How can I save the plot data (X, Y points) as a CSV?

**A**: The application does not have a built‑in export for plot data. You can extract the data from the DataModel and save it with pandas:

```python
import pandas as pd
from csv_plotter.model.data_model import DataModel

model = DataModel(df)
x = model.get_column('XColumn')
y = model.get_column('YColumn')
pd.DataFrame({'X': x, 'Y': y}).to_csv('plot_data.csv', index=False)
```

### Q: Can I add custom plot types (e.g., 3D scatter)?

**A**: Yes, but 3D plotting requires `mpl_toolkits.mplot3d`. The current canvas is 2D only. Adding 3D support would involve modifying `PlotCanvas` to create a 3D axis and updating the controller accordingly.

### Q: Why is the table limited to 1000 rows?

**A**: Performance and responsiveness. Displaying tens of thousands of rows in a Qt table can be slow. The limit is defined in `constants.MAX_TABLE_ROWS`. You can increase it, but be aware of potential slowdowns.

### Q: How do I report a bug or request a feature?

**A**: Please open an issue on the project’s GitHub repository. Include:

- Steps to reproduce the bug.
- Expected vs actual behavior.
- Screenshots if applicable.
- Your operating system, Python version, and versions of PyQt5, matplotlib, pandas.

## Getting Further Help

If you have a problem not covered here, try:

- Reading the [User Guide](user_guide.md) and [Developer Guide](developer_guide.md).
- Searching the source code for relevant error messages.
- Checking the [test report](../TEST_REPORT.md) to see if your scenario is covered by tests.
- Asking on community forums (Stack Overflow, Reddit) with the tag `pyqt5` or `matplotlib`.

You can also contact the maintainers via the GitHub repository.