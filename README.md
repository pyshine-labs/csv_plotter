# CSV Drag‑and‑Drop Plotting Application

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

A standalone desktop application built with PyQt5 that allows users to drag and drop CSV files, preview the data in a table, select columns, and generate interactive plots using matplotlib. The application follows a Model‑View‑Controller (MVC)‑like pattern to separate data handling, UI, and plotting logic.

## 📋 Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Tutorial](#usage-tutorial)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Development](#development)
- [Packaging](#packaging)
- [Troubleshooting](#troubleshooting)
- [Documentation](#documentation)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## ✨ Features

- **Drag‑and‑drop CSV files** – Simply drag a `.csv` or `.txt` file onto the application window.
- **Smart CSV parsing** – Automatic detection of delimiter, header row, and encoding using chardet.
- **Data table view** – Browse your CSV data with sortable columns, numeric highlighting, and alternating row colors.
- **Interactive plotting** – Scatter, line, bar, histogram, and box plots with customizable styling.
- **Plot customization** – Choose X/Y columns, axis labels, titles, grid, legend, colors, and markers.
- **Embedded matplotlib toolbar** – Zoom, pan, save, reset view, and adjust subplots.
- **Theme support** – Light and dark UI themes with seamless switching.
- **Export plots** – Save plots as PNG, JPEG, PDF, or SVG via the toolbar or menu.
- **Error handling** – Informative error messages for malformed CSV, missing data, and unsupported operations.
- **Sample data** – Includes a sample CSV file for immediate testing.

## 📦 Requirements

- Python 3.7 or higher
- PyQt5 >= 5.15
- matplotlib >= 3.5
- pandas >= 1.3
- numpy >= 1.20
- chardet >= 4.0

All dependencies are listed in [`requirements.txt`](requirements.txt).

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/csv-drag-drop-plotter.git
cd csv-drag-drop-plotter
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Alternatively, install the package in development mode (optional):

```bash
pip install -e .
```

## 🎯 Quick Start

After installation, run the application with either of the following commands:

```bash
python run.py
```

or

```bash
python -m csv_plotter.src.main
```

The main window will appear. Drag a CSV file onto the drop area to begin.

## 📖 Usage Tutorial

### 1. Loading a CSV file

- **Drag and drop**: Drag any CSV file from your file manager and drop it onto the large drop area in the top‑left of the window.
- **File menu**: Use **File → Open** (`Ctrl+O`) to browse for a CSV file.

Once loaded, the data table will display the first few rows, and the column selection combos will be populated.

### 2. Exploring the data

- The table is fully sortable: click any column header to sort ascending/descending.
- Use the scrollbars to navigate through large datasets.
- The status bar shows the number of rows and columns loaded.

### 3. Creating a plot

1. **Select columns**: In the right‑side control panel, choose an X‑axis column and a Y‑axis column from the dropdown menus.
2. **Choose plot type**: Select one of the available plot types (Scatter, Line, Bar, Histogram, Box).
3. **Customize options** (optional):
   - Set axis labels and plot title.
   - Toggle grid lines.
   - Adjust colors, markers, and line styles.
4. **Generate plot**:
   - Click the **Update Plot** button.
   - If **Auto‑update** is enabled (checkbox), the plot will refresh automatically after any selection change.

### 4. Interacting with the plot

The matplotlib toolbar below the plot provides:

- **Zoom**: Click the magnifying glass, then drag a rectangle to zoom in.
- **Pan**: Click the hand icon, then drag to pan the view.
- **Save**: Save the current plot as PNG, JPEG, PDF, or SVG.
- **Home**: Return to the original view.
- **Forward/Back**: Navigate through previous views.

### 5. Changing themes

Switch between light and dark themes via **View → Theme → Light/Dark**. The change applies instantly to the entire UI.

### 6. Exporting a plot

- Use the **Save** button in the toolbar.
- Or choose **File → Export Plot** (`Ctrl+S`) to select format and location.

## 📸 Screenshots

*(Placeholder: actual screenshots can be added later)*

- **Main Window (Light Theme)**: Shows the drop area, data table, control panel, and an empty plot canvas.
- **Loaded Data**: A CSV file with numeric columns displayed in the table, column combos populated.
- **Scatter Plot Example**: A scatter plot with grid, axis labels, and title.
- **Dark Theme**: The same interface with a dark color scheme.

## 📁 Project Structure

```
csv_plotter/
├── src/                          # Source code
│   ├── ui/                       # PyQt5 widgets
│   │   ├── main_window.py        # Main application window
│   │   ├── drop_area.py          # Drag‑and‑drop area
│   │   ├── control_panel.py      # Right‑side control panel
│   │   └── theme.py              # Theme manager
│   ├── model/                    # Data handling
│   │   ├── csv_parser.py         # CSV parsing with delimiter/encoding detection
│   │   ├── data_model.py         # Data model wrapper for DataFrame
│   │   └── table_model.py        # PyQt table model for pandas DataFrame
│   ├── plot/                     # Plotting logic
│   │   ├── plot_canvas.py        # Matplotlib canvas with toolbar
│   │   └── plot_controller.py    # Controller that orchestrates plotting
│   └── utils/                    # Utilities
│       └── constants.py          # Application constants
├── resources/                    # Icons, stylesheets, sample data
├── tests/                        # Unit and integration tests
├── docs/                         # Documentation (user guide, developer guide)
├── requirements.txt              # Python dependencies
├── run.py                        # Convenience launch script
├── setup.py                      # Package setup (optional)
└── README.md                     # This file
```

For a detailed architectural overview, see the [Architecture Document](plans/csv_plotter_architecture.md).

## 🛠 Development

### Running Tests

The project uses `pytest` and `pytest‑qt` for testing. To run the full test suite:

```bash
pytest tests/
```

To run with coverage report:

```bash
pytest --cov=src tests/
```

The latest test report is available at [`TEST_REPORT.md`](TEST_REPORT.md).

### Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/).
- Use type hints where appropriate.
- Write docstrings for all public classes and functions (Google style).

### Adding New Features

- **New plot type**: Extend `PlotController` and add the drawing logic in `PlotCanvas`.
- **New file format**: Implement a new parser in `model/` and integrate it with the `CSVParser` interface.
- **UI customization**: Modify the Qt widgets in `ui/` and update the stylesheets in `resources/styles/`.

Refer to the [Developer Guide](docs/developer_guide.md) for detailed instructions.

## 📦 Packaging

### Creating a Standalone Executable with PyInstaller

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Build the executable (one‑file, windowed):

```bash
pyinstaller --onefile --windowed --name CSVPlotter csv_plotter/src/main.py
```

The executable will be placed in the `dist/` folder. You can distribute this file to users who do not have Python installed.

### Creating a Python Package

The project includes a `setup.py` file for packaging as a Python library (optional). To install in development mode:

```bash
pip install -e .
```

## 🚨 Troubleshooting

### Common Issues

- **PyQt5 installation fails**: On some Linux distributions, you may need to install system packages: `sudo apt-get install python3-pyqt5`.
- **Missing matplotlib backend**: Ensure you have a GUI backend (e.g., `PyQt5`, `TkAgg`) installed. The application uses `PyQt5Agg`.
- **CSV parsing errors**: The parser tries multiple encodings; if your file still fails, try converting it to UTF‑8.
- **Application crashes on launch**: Check that all dependencies are installed correctly: `pip install -r requirements.txt`.

### Getting Help

If you encounter a bug or have a feature request, please open an issue on the GitHub repository.

## 📚 Documentation

- **[User Guide](docs/user_guide.md)** – Step‑by‑step instructions for end‑users.
- **[Developer Guide](docs/developer_guide.md)** – How to extend and contribute to the project.
- **[API Overview](docs/api_overview.md)** – Summary of key classes and functions.
- **[Architecture Document](plans/csv_plotter_architecture.md)** – High‑level design and component interactions.
- **[Test Report](TEST_REPORT.md)** – Results of the comprehensive test suite.
- **[Packaging Guide](docs/packaging.md)** – How to create standalone executables with PyInstaller.
- **[Troubleshooting Guide](docs/troubleshooting.md)** – Solutions to common problems and FAQs.
- **[Changelog](CHANGELOG.md)** – History of changes and releases.

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE.md) file for details.

## 🙏 Acknowledgments

- Built with [PyQt5](https://www.riverbankcomputing.com/software/pyqt/), [matplotlib](https://matplotlib.org/), and [pandas](https://pandas.pydata.org/).
- Icons from [Material Design Icons](https://materialdesignicons.com/) (optional).
- Inspired by the need for a simple, interactive CSV visualization tool for data scientists and analysts.