# Packaging the Application

This guide explains how to package the CSV Drag‑and‑Drop Plotter into a standalone executable that can be distributed to users who do not have Python installed. We use **PyInstaller**, a popular tool that bundles Python applications and their dependencies into a single folder or file.

## Prerequisites

- The application must run correctly in your development environment.
- Install PyInstaller:

```bash
pip install pyinstaller
```

- (Optional) Install UPX (Ultimate Packer for eXecutables) to reduce executable size. Download from [upx.github.io](https://upx.github.io/) and ensure the `upx` command is in your PATH.

## Basic Packaging

### 1. Create a Simple One‑File Executable

Run PyInstaller from the project root directory (where `run.py` is located):

```bash
pyinstaller --onefile --windowed --name CSVPlotter csv_plotter/src/main.py
```

**Explanation of options**:

- `--onefile`: Package everything into a single executable file.
- `--windowed`: Prevent a console window from appearing (Windows/macOS). On Linux, this option suppresses the terminal window if using a GUI.
- `--name CSVPlotter`: Set the output executable name to `CSVPlotter` (or `CSVPlotter.exe` on Windows).
- `csv_plotter/src/main.py`: The entry point script.

The resulting executable will be placed in the `dist/` folder.

### 2. Test the Executable

Navigate to `dist/` and run the executable:

```bash
./CSVPlotter          # macOS/Linux
CSVPlotter.exe        # Windows
```

If the application launches successfully, try loading a CSV file and generating a plot. If it fails, check the “Troubleshooting” section below.

## Advanced Packaging Options

### Include Data Files (Resources)

The application uses resources such as icons, stylesheets, and sample data located in `csv_plotter/resources/`. By default, PyInstaller does not bundle these files, causing runtime errors when the application tries to load them.

To include the resources, create a **spec file** and add `datas`.

First, generate a spec file:

```bash
pyinstaller --onefile --windowed --name CSVPlotter csv_plotter/src/main.py
```

This creates `CSVPlotter.spec`. Edit it and add a `datas` list to the `Analysis` object:

```python
# CSVPlotter.spec
a = Analysis(
    ['csv_plotter/src/main.py'],
    pathex=[],
    binaries=[],
    datas=[('csv_plotter/resources', 'csv_plotter/resources')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    ...
)
```

The tuple `('csv_plotter/resources', 'csv_plotter/resources')` means “copy the entire `resources` folder and place it under the same relative path in the bundled app”.

If you only need sample data and icons, you can specify subfolders:

```python
datas=[
    ('csv_plotter/resources/icons', 'csv_plotter/resources/icons'),
    ('csv_plotter/resources/sample_data', 'csv_plotter/resources/sample_data'),
],
```

After editing the spec file, rebuild using the spec:

```bash
pyinstaller CSVPlotter.spec
```

### Include Hidden Imports

Sometimes PyInstaller fails to detect certain imports (e.g., PyQt5 modules, pandas submodules). If you encounter `ModuleNotFoundError` at runtime, add those modules as hidden imports:

```python
hiddenimports=['pandas._libs.tslibs.timedeltas', 'PyQt5.QtCore', 'PyQt5.QtGui'],
```

You can also specify them on the command line:

```bash
pyinstaller --onefile --windowed --hidden-import pandas._libs.tslibs.timedeltas --hidden-import PyQt5.QtCore csv_plotter/src/main.py
```

### Exclude Unnecessary Modules

To reduce the size of the executable, you can exclude modules that are not used (e.g., `tkinter`, `numpy.testing`):

```python
excludes=['tkinter', 'numpy.testing', 'matplotlib.tests', 'pandas.tests'],
```

### Set the Application Icon

To give the executable a custom icon, use the `--icon` option (requires a `.ico` file on Windows, `.icns` on macOS, or `.png` on Linux).

```bash
pyinstaller --onefile --windowed --icon=resources/icons/app_icon.ico --name CSVPlotter csv_plotter/src/main.py
```

## Platform‑Specific Instructions

### Windows

- **One‑file executable**: Works well. The executable may be flagged by antivirus software because it’s a packed Python app. You can sign the executable with a code‑signing certificate to avoid warnings.
- **Console window**: If you omit `--windowed`, a console window will open alongside the GUI (useful for debugging). For production, keep `--windowed`.
- **DLL issues**: If you see errors about missing DLLs (e.g., `VCRUNTIME140.dll`), ensure the Microsoft Visual C++ Redistributable is installed on the target machine. You can embed it with PyInstaller using `--add‑binary`.

### macOS

- **App bundle**: To create a `.app` bundle instead of a plain executable, use `--windowed` and PyInstaller will generate `CSVPlotter.app`.

  ```bash
  pyinstaller --windowed --name CSVPlotter csv_plotter/src/main.py
  ```

  The bundle will be in `dist/CSVPlotter.app`. You can customize its `Info.plist` via the spec file.

- **Code signing**: To distribute on macOS, you must sign the app with an Apple Developer ID. Use `codesign`:

  ```bash
  codesign --deep --force --verify --verbose --sign "Developer ID Application: Your Name" dist/CSVPlotter.app
  ```

- **Gatekeeper**: Unsigned apps may be blocked. You can notarize the app using `xcrun notarytool`.

### Linux

- **Dependencies**: The bundled executable may still depend on system libraries (e.g., `libX11`, `libGL`). Ensure those libraries are present on the target system.
- **AppImage**: Consider building an [AppImage](https://appimage.org/) for portable distribution. Tools like `linuxdeploy` can help.
- **Desktop entry**: You can create a `.desktop` file for integration with application menus.

## Creating an Installer

After you have a working executable (or app bundle), you may want to create an installer for easier distribution.

- **Windows**: Use [Inno Setup](https://jrsoftware.org/isinfo.php) or [NSIS](https://nsis.sourceforge.io/).
- **macOS**: Use [create‑dmg](https://github.com/create-dmg/create-dmg) to create a DMG disk image.
- **Linux**: Use `deb`/`rpm` packages or the aforementioned AppImage.

## Testing the Packaged Application

Always test the packaged application on a **clean machine** (or a virtual machine) that does not have Python or the dependencies installed. This ensures that all required files are correctly bundled.

### Common Issues and Solutions

| Issue | Possible Cause | Solution |
|-------|---------------|----------|
| “Failed to execute script main” | Missing module or resource. | Run with `--debug` to see detailed error: `pyinstaller --debug all ...`. Add missing hidden imports or datas. |
| Application starts but CSV loading fails | Resources not included. | Add the `resources` folder to `datas` in the spec file. |
| Plot canvas blank | matplotlib backend not properly bundled. | Force the backend by setting `MPLBACKEND=Qt5Agg` in the environment before launching, or patch the matplotlib configuration in your code. |
| Large executable size (500 MB+) | PyInstaller includes many unnecessary libraries. | Use `--exclude‑module` to remove unused modules, and consider using UPX compression. |
| Slow startup | One‑file executable extracts to a temporary directory each time. | Consider using a one‑folder distribution (`--onedir`) for faster startup, but with more files. |

## Example Spec File

Below is a complete example `CSVPlotter.spec` that includes resources, hidden imports, and excludes.

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['csv_plotter/src/main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('csv_plotter/resources', 'csv_plotter/resources'),
        ('csv_plotter/src', 'csv_plotter/src'),
    ],
    hiddenimports=[
        'pandas._libs.tslibs.timedeltas',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'matplotlib.backends.backend_qt5agg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'numpy.testing', 'matplotlib.tests', 'pandas.tests'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CSVPlotter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,          # change to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

## Continuous Integration (CI) Packaging

You can automate packaging using CI services (GitHub Actions, GitLab CI, etc.). A typical workflow:

1. Install Python and dependencies.
2. Run `pyinstaller` with the spec file.
3. Upload the resulting executable as a release artifact.

Refer to the [PyInstaller documentation](https://pyinstaller.org/en/stable/) for advanced options and best practices.

---

*Packaging is an iterative process. Test thoroughly on each target platform before distributing to users.*