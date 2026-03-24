# CSV Drag‑and‑Drop Plotter – User Guide

This guide provides detailed instructions for using the CSV Drag‑and‑Drop Plotting Application. Whether you are a data analyst, researcher, or student, this tool will help you quickly visualize CSV data with minimal setup.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Launching the Application](#launching-the-application)
- [User Interface Overview](#user-interface-overview)
- [Loading Data](#loading-data)
- [Exploring the Data Table](#exploring-the-data-table)
- [Creating Plots](#creating-plots)
- [Customizing Plots](#customizing-plots)
- [Interacting with the Plot](#interacting-with-the-plot)
- [Switching Themes](#switching-themes)
- [Exporting Plots](#exporting-plots)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [Troubleshooting](#troubleshooting)
- [FAQs](#faqs)

## Introduction

The CSV Drag‑and‑Drop Plotter is a desktop application that lets you:

- Drag and drop CSV files directly onto the window.
- View the data in a sortable, scrollable table.
- Select columns for the X and Y axes.
- Generate scatter, line, bar, histogram, and box plots.
- Customize plot appearance (labels, titles, colors, grid).
- Save plots as image files (PNG, JPEG, PDF, SVG).

It is built with Python, PyQt5, and matplotlib, offering a responsive and intuitive interface.

## Installation

### Prerequisites

- **Python 3.7 or higher** – Download from [python.org](https://www.python.org/).
- **pip** – Usually included with Python.

### Step‑by‑Step Installation

1. **Download the application**  
   Clone the repository or download the source code as a ZIP file.

2. **Open a terminal** and navigate to the folder containing `requirements.txt`.

3. **Create a virtual environment (recommended)**  
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

   This installs PyQt5, matplotlib, pandas, numpy, and chardet.

5. **Verify installation**  
   Run the application once to ensure everything works (see [Launching the Application](#launching-the-application)).

## Launching the Application

After installation, you can start the application in two ways:

### Option 1 – Using the convenience script
```bash
python run.py
```

### Option 2 – Direct module execution
```bash
python -m csv_plotter.src.main
```

The main window will appear after a few seconds. You should see a large drop‑area, an empty data table, a control panel, and a blank plot canvas.

## User Interface Overview

The main window is divided into four main regions:

1. **Menu Bar** – File, Edit, View, Theme, Help menus.
2. **Toolbar** – Quick‑access buttons for Open, Save, Export, Theme toggle, and Help.
3. **Top Splitter** (left‑right):
   - **Left side**: Drop area (top) and data table (bottom).
   - **Right side**: Control panel with column selection, plot type, and customization options.
4. **Bottom Section**: Matplotlib canvas with its own interactive toolbar.

![UI Overview](resources/screenshots/ui_overview.png) *(placeholder)*

### Menu Bar Actions

- **File** → Open, Export Plot, Exit.
- **Edit** → Copy Plot (copies the current plot to clipboard).
- **View** → Toggle Table/Plot visibility, Switch theme (Light/Dark).
- **Help** → About, User Guide.

### Toolbar Buttons

| Icon | Action | Description |
|------|--------|-------------|
| 📁 | Open | Open a CSV file via file dialog |
| 💾 | Save | Save the current plot |
| 🎨 | Theme | Toggle between light and dark themes |
| ❓ | Help | Open the user guide |

## Loading Data

### Drag and Drop

1. Open your file manager (Windows Explorer, Finder, Nautilus, etc.).
2. Select a CSV file (or any text file with delimiter‑separated values).
3. Drag the file and drop it onto the **drop area** (the large rectangle with the cloud‑upload icon and hint text).
4. The application will parse the file, detect its delimiter and encoding, and load the data.

### Using the File Dialog

1. Click the **Open** button on the toolbar, or choose **File → Open** (`Ctrl+O`).
2. Navigate to your CSV file and click **Open**.

### Supported File Formats

- **.csv** – Comma‑separated values.
- **.txt** – Tab‑separated values or other delimiters (automatically detected).
- **.tsv** – Tab‑separated values (treated as `.txt`).

The parser expects the first row to be a header (column names). If your file has no header, the parser will assign generic names (Column1, Column2, …).

### Sample Data

The application includes a sample CSV file at `resources/sample_data/sample.csv`. You can use it to test the application without your own data.

## Exploring the Data Table

Once a CSV file is loaded, the table view displays the first 1000 rows (for performance). The table provides the following features:

- **Sorting**: Click a column header to sort ascending; click again for descending.
- **Scrollbars**: Use vertical and horizontal scrollbars to navigate large datasets.
- **Alternating row colors**: Improves readability.
- **Cell tooltips**: Hover over a cell to see its full content if truncated.

The status bar shows the number of rows and columns loaded, e.g., “Loaded 250 rows × 5 columns”.

## Creating Plots

### Step 1 – Select Columns

In the control panel, you will see two dropdown menus labeled **X‑Axis Column** and **Y‑Axis Column**. They are populated with the column names from your CSV.

- Choose one column for the X‑axis (e.g., “Time”, “Index”).
- Choose another column for the Y‑axis (e.g., “Temperature”, “Sales”).

For histogram plots, only the X‑axis column is used (Y‑axis is ignored). For box plots, the Y‑axis column is used to group data.

### Step 2 – Choose Plot Type

Select one of the five plot types from the **Plot Type** dropdown:

- **Scatter** – Points for each (X, Y) pair.
- **Line** – Connected line through (X, Y) points (ordered by X).
- **Bar** – Vertical bars for each X value (Y as height).
- **Histogram** – Distribution of values in the X column (bins).
- **Box** – Box‑and‑whisker plot of the Y column (grouped by X if multiple groups).

### Step 3 – Adjust Basic Options

- **Axis Labels**: Enter text for the X‑axis label and Y‑axis label (optional).
- **Plot Title**: Enter a title for the plot.
- **Grid**: Check “Show Grid” to add a background grid.
- **Legend**: Check “Show Legend” to display a legend (when multiple series are present).

### Step 4 – Generate the Plot

Click the **Update Plot** button. The plot canvas will refresh with the new visualization.

**Auto‑update**: If you enable the “Auto‑update” checkbox, the plot will update automatically every time you change a column selection, plot type, or any option. This is useful for rapid exploration.

## Customizing Plots

### Styling Options

The control panel also provides styling options (expandable section):

- **Point Style** (scatter plots): Marker shape (circle, square, triangle, etc.), size, and color.
- **Line Style** (line plots): Line width, dash pattern, and color.
- **Bar Style** (bar plots): Bar color, edge color, and width.
- **Histogram Style**: Number of bins, bar color, edge color.
- **Box Style**: Box color, whisker style, outlier markers.

### Advanced Customization

You can directly interact with the matplotlib toolbar to adjust the plot after generation:

- Use the **Configure Subplots** button to adjust margins, spacing, and figure size.
- Use the **Edit Axis** button (if available) to modify axis limits, scales (linear/log), and tick labels.

These advanced features are part of the standard matplotlib toolbar and are documented in the [matplotlib documentation](https://matplotlib.org/stable/users/index.html).

## Interacting with the Plot

The matplotlib toolbar below the plot canvas provides the following tools:

| Button | Name | Action |
|--------|------|--------|
| 🏠 | Home | Restore the original view |
| ↔️ | Forward/Back | Navigate through previous views |
| 🔍 | Zoom | Click‑and‑drag a rectangle to zoom in |
| ✋ | Pan | Click‑and‑drag to pan the view |
| 💾 | Save | Save the plot to a file |
| ⚙️ | Configure Subplots | Adjust subplot parameters |
| 📋 | Copy | Copy the plot to clipboard (not always available) |

**Zooming**: Click the magnifying glass, then click and drag a rectangle over the region you want to zoom into. Right‑click to zoom out.

**Panning**: Click the hand icon, then click and drag the plot to move it.

**Reset**: Click the **Home** button to return to the initial view.

## Switching Themes

The application supports two visual themes: **Light** (default) and **Dark**. To switch:

- Go to **View → Theme → Light** (or **Dark**).
- Or click the **Theme** button on the toolbar (toggles between light/dark).

The change is immediate and affects all UI elements: window background, text colors, table colors, button styles, etc.

## Exporting Plots

You can save the current plot as an image or vector graphic in several formats.

### Using the Toolbar Save Button

1. Ensure the plot is displayed as you want it.
2. Click the **Save** button (floppy‑disk icon) on the matplotlib toolbar.
3. In the file dialog, choose a location, enter a filename, and select a format (PNG, JPEG, PDF, SVG).
4. Click **Save**.

### Using the Menu

- **File → Export Plot** (`Ctrl+S`) opens the same dialog.

### Export Settings

The saved image will have the same dimensions as the plot canvas on your screen. For higher resolution, you can resize the main window before saving (the canvas will scale accordingly).

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open a CSV file |
| `Ctrl+S` | Export the current plot |
| `Ctrl+C` | Copy plot to clipboard (if supported) |
| `Ctrl+Q` | Quit the application |
| `F1` | Open this user guide |

## Troubleshooting

### The application won’t start

- Ensure Python 3.7+ is installed and accessible from the terminal (`python --version`).
- Verify all dependencies are installed: `pip list` should show PyQt5, matplotlib, pandas, numpy, chardet.
- On macOS, if you see “PyQt5.QtCore” not found, try reinstalling PyQt5: `pip install --force-reinstall PyQt5`.

### CSV file fails to load

- Check that the file is not empty.
- Try opening the file in a text editor to verify it is a valid CSV.
- If the file uses a non‑standard delimiter (e.g., semicolon), the parser will detect it automatically. However, if detection fails, you can convert the file to comma‑separated format.
- If the file contains non‑ASCII characters, ensure the encoding is supported (UTF‑8, Latin‑1, etc.). The parser tries multiple encodings, but you may need to convert the file to UTF‑8.

### Plot appears empty or incorrect

- Verify that the selected columns contain numeric data. Non‑numeric columns are ignored.
- For histogram plots, ensure the X‑axis column is numeric.
- If the plot looks scrambled, check for missing values (NaN) in the data; they may cause gaps.

### The table shows only a subset of rows

The table is limited to 1000 rows for performance reasons. The plot uses the full dataset, but the table display is capped. You can adjust this limit in the source code if needed.

## FAQs

**Q: Can I plot multiple Y columns against the same X column?**  
A: Not directly in the current version. You can load the file multiple times or modify the code to support multiple series.

**Q: Does the application support real‑time data streaming?**  
A: No, it is designed for static CSV files. However, you could extend it to watch a folder for new CSV files.

**Q: Can I change the language of the UI?**  
A: The UI is currently only in English. Internationalization could be added by contributing translations.

**Q: Is there a command‑line interface?**  
A: No, the application is purely graphical. However, you can automate loading and plotting via Python scripts using the underlying modules.

**Q: How can I report a bug or suggest a feature?**  
A: Please open an issue on the project’s GitHub repository.

---

*For developers interested in extending the application, refer to the [Developer Guide](developer_guide.md).*