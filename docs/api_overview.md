# API Overview

This document provides a high‑level summary of the public API of the CSV Drag‑and‑Drop Plotter. For detailed docstrings and implementation, refer to the source code.

The API is organized into four main modules:

- **`model`** – Data loading and manipulation.
- **`ui`** – PyQt5 widgets and windows.
- **`plot`** – Matplotlib plotting and control.
- **`utils`** – Constants and helper functions.

---

## Model Module

### `csv_parser.CSVParser`

The main CSV parsing class.

**Methods**:

- `load(file_path: str) -> pandas.DataFrame`  
  Load a CSV file, automatically detecting delimiter, encoding, and header. Raises `ValueError` if parsing fails, `FileNotFoundError` if the file does not exist, or `EmptyDataError` if the file is empty.

- `_detect_encoding(file_path: str) -> str` (protected)  
  Guess the file encoding using `chardet`.

- `_guess_dialect(file_path: str, encoding: str) -> Tuple[str, bool]` (protected)  
  Determine the delimiter and whether the file has a header row.

### `data_model.DataModel`

Wrapper around a pandas DataFrame that provides structured access and additional metadata.

**Methods**:

- `__init__(dataframe: pandas.DataFrame)`  
  Initialize with a DataFrame.

- `dataframe` (property) -> pandas.DataFrame  
  Return a copy of the internal DataFrame (prevents mutation).

- `columns` (property) -> List[str]  
  Return the column names.

- `shape` (property) -> Tuple[int, int]  
  Return (rows, columns).

- `get_column(column_name: str) -> pandas.Series`  
  Return the Series for a given column.

- `get_summary() -> Dict[str, Any]`  
  Return a dictionary with basic statistics (mean, std, min, max, etc.) for numeric columns.

- `has_numeric(column_name: str) -> bool`  
  Check whether a column contains numeric data.

### `table_model.PandasTableModel`

A Qt table model that adapts a pandas DataFrame for display in a `QTableView`.

**Methods**:

- `__init__(dataframe: pandas.DataFrame)`  
  Initialize with a DataFrame.

- `rowCount(parent: QModelIndex = ...) -> int`  
  Return the number of rows.

- `columnCount(parent: QModelIndex = ...) -> int`  
  Return the number of columns.

- `data(index: QModelIndex, role: int = Qt.DisplayRole) -> Any`  
  Return the cell data for the given index and role.

- `headerData(section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole) -> Any`  
  Return column or row header text.

- `sort(column: int, order: Qt.SortOrder) -> None`  
  Sort the DataFrame by the selected column.

---

## UI Module

### `main_window.MainWindow`

The main application window (subclass of `QMainWindow`).

**Signals**:

- `data_loaded()` – emitted when a CSV file is successfully loaded.

**Methods**:

- `__init__(parent: Optional[QWidget] = None)`  
  Create the window and initialize all UI components.

- `_init_ui() -> None` (protected) – set up the layout, widgets, menu, toolbar.
- `_connect_signals() -> None` (protected) – connect signals and slots.
- `_create_menu_bar() -> None` (protected) – create the menu bar.
- `_create_toolbar() -> None` (protected) – create the toolbar.
- `_update_ui_state(has_data: bool) -> None` (protected) – enable/disable UI elements based on whether data is loaded.

- `on_file_dropped(file_path: str) -> None`  
  Handle a dropped CSV file: parse, update data model, refresh table and control panel.

- `update_plot() -> None`  
  Trigger a plot update based on current selections.

### `drop_area.DropArea`

A custom widget that accepts drag‑and‑drop of CSV files.

**Signals**:

- `file_dropped_signal(str)` – emitted with the file path when a file is dropped.

**Methods**:

- `dragEnterEvent(event: QDragEnterEvent) -> None` – highlight the widget when a drag enters.
- `dropEvent(event: QDropEvent) -> None` – process the dropped file and emit the signal.

### `control_panel.ControlPanel`

The right‑side panel containing column selection, plot type, and styling options.

**Signals**:

- `selection_changed_signal()` – emitted when any selection (X column, Y column, plot type) changes.

**Methods**:

- `__init__(parent: Optional[QWidget] = None)`  
  Create the panel with all child widgets.

- `set_columns(columns: List[str]) -> None`  
  Populate the X and Y column combo boxes.

- `get_selections() -> Tuple[str, str, str]`  
  Return (x_column, y_column, plot_type).

- `get_options() -> Dict[str, Any]`  
  Return a dictionary of styling options (axis labels, title, grid, etc.).

- `set_auto_update(state: bool) -> None`  
  Enable/disable the auto‑update checkbox.

### `theme.ThemeManager`

Manages UI themes (light/dark).

**Methods**:

- `__init__(app: QApplication)`  
  Initialize with a reference to the application.

- `apply_theme(theme_name: str) -> None`  
  Apply a theme by name (currently “light” or “dark”).

- `toggle_theme() -> None`  
  Switch between light and dark.

- `current_theme` (property) -> str  
  Return the name of the currently active theme.

---

## Plot Module

### `plot_canvas.PlotCanvas`

A matplotlib figure canvas embedded in a PyQt5 widget, with an attached navigation toolbar.

**Methods**:

- `__init__(parent: Optional[QWidget] = None)`  
  Create the canvas and toolbar.

- `draw_plot(x_data: pandas.Series, y_data: pandas.Series, plot_type: str, **kwargs) -> None`  
  Draw a plot of the given type using the provided data series.  
  Supported `plot_type` values: `"scatter"`, `"line"`, `"bar"`, `"histogram"`, `"box"`.

- `clear() -> None`  
  Clear the canvas (remove all artists).

- `save_plot(path: str, fmt: str = "png") -> None`  
  Save the current figure to a file. `fmt` can be “png”, “jpg”, “pdf”, “svg”.

- `get_figure() -> matplotlib.figure.Figure`  
  Return the underlying matplotlib figure (for advanced manipulation).

### `plot_controller.PlotController`

Orchestrates plot generation: retrieves data from the DataModel, passes it to the PlotCanvas, and applies styling options.

**Methods**:

- `__init__(data_model: DataModel, plot_canvas: PlotCanvas)`  
  Initialize with references to the data model and canvas.

- `set_selections(x_column: str, y_column: str, plot_type: str) -> None`  
  Set the columns and plot type for the next plot.

- `set_options(**kwargs) -> None`  
  Set styling options (title, axis labels, grid, colors, etc.).

- `generate_plot() -> None`  
  Generate the plot with the current selections and options.

- `_generate_plot() -> None` (protected) – internal method that calls the appropriate drawing routine.

---

## Utils Module

### `constants`

A module containing application‑wide constants.

**Constants**:

- `APP_NAME = "CSV Drag‑and‑Drop Plotter"`
- `SUPPORTED_FORMATS = ["csv", "txt"]`
- `THEMES = ["light", "dark"]`
- `PLOT_TYPES = ["scatter", "line", "bar", "histogram", "box"]`
- `MAX_TABLE_ROWS = 1000`

---

## Entry Points

### `main.main()`

The application entry point. Calls `ui.main_window.main()`.

### `ui.main_window.main()`

Creates the `QApplication`, instantiates the `MainWindow`, and starts the event loop.

---

## Auto‑generated API Documentation

The source code includes comprehensive docstrings that can be used to generate HTML API documentation with tools such as:

- **pdoc**: `pdoc --html csv_plotter.src`
- **Sphinx**: Requires a `docs/conf.py` configuration.

To generate API docs with pdoc:

```bash
pip install pdoc
pdoc --html csv_plotter.src --output-dir docs/api
```

The generated documentation will be placed in `docs/api/`.

---

*This overview is based on the source code as of version 1.0. For the most up‑to‑date information, inspect the docstrings directly.*