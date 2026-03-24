"""
Unit tests for ControlPanel widget.
"""
import pytest
from PyQt5.QtCore import Qt
from src.ui.control_panel import ControlPanel


@pytest.fixture
def control_panel(qtbot):
    """Create a ControlPanel instance."""
    panel = ControlPanel()
    qtbot.addWidget(panel)
    return panel


def test_initial_state(control_panel):
    """Test default selections."""
    assert control_panel.x_column() is None
    assert control_panel.y_column() is None
    assert control_panel.plot_type() == 'scatter'
    # Check default options
    opts = control_panel.options()
    assert opts['grid'] == True
    assert opts['legend'] == False
    assert opts['x_label'] == ''
    assert opts['y_label'] == ''
    assert opts['title'] == ''


def test_set_columns(control_panel):
    """Test populating column combos."""
    columns = ['Col1', 'Col2', 'Col3', 'Col4']
    control_panel.set_columns(columns)
    # Combos should contain all columns
    assert control_panel.x_combo.count() == 4
    assert control_panel.y_combo.count() == 4
    # First two columns auto‑selected
    assert control_panel.x_column() == 'Col1'
    assert control_panel.y_column() == 'Col2'
    # Label combos also populated
    assert control_panel.x_label_edit.count() == 4
    assert control_panel.y_label_edit.count() == 4
    # Title suggestions
    assert control_panel.title_edit.count() > 0


def test_set_columns_single_column(control_panel):
    """Test with only one column."""
    control_panel.set_columns(['Only'])
    assert control_panel.x_column() == 'Only'
    assert control_panel.y_column() is None  # second combo empty
    # y_combo has one item but current index is -1? Let's check
    # Since there is only one column, y_combo has 'Only' but maybe not selected
    # Implementation selects y only if len >=2
    # So y_column() returns None
    assert control_panel.y_combo.currentIndex() == -1


def test_set_columns_empty(control_panel):
    """Test with empty column list."""
    control_panel.set_columns([])
    assert control_panel.x_combo.count() == 0
    assert control_panel.y_combo.count() == 0
    assert control_panel.x_column() is None
    assert control_panel.y_column() is None


def test_set_selection(control_panel):
    """Test programmatically setting selection."""
    columns = ['A', 'B', 'C']
    control_panel.set_columns(columns)
    control_panel.set_selection('B', 'C', 'Line')
    assert control_panel.x_column() == 'B'
    assert control_panel.y_column() == 'C'
    assert control_panel.plot_type() == 'line'
    # Unknown column should be ignored
    control_panel.set_selection('Missing', 'A', 'Bar')
    # x column stays 'B' because missing column not found
    assert control_panel.x_column() == 'B'


def test_options_reflect_ui(control_panel, qtbot):
    """Test that options() returns current UI state."""
    control_panel.set_columns(['X', 'Y'])
    # Change UI elements
    control_panel.grid_check.setChecked(False)
    control_panel.legend_check.setChecked(True)
    control_panel.x_label_edit.setCurrentText('X axis')
    control_panel.y_label_edit.setCurrentText('Y axis')
    control_panel.title_edit.setCurrentText('My Plot')
    opts = control_panel.options()
    assert opts['grid'] == False
    assert opts['legend'] == True
    assert opts['x_label'] == 'X axis'
    assert opts['y_label'] == 'Y axis'
    assert opts['title'] == 'My Plot'


def test_plot_requested_signal(control_panel, qtbot):
    """Test that clicking update button emits plot_requested."""
    with qtbot.waitSignal(control_panel.plot_requested, timeout=1000):
        control_panel.update_button.click()


def test_selection_changed_signal(control_panel, qtbot):
    """Test that changing combos triggers internal slot (no emission)."""
    # The internal slot does nothing; we just ensure no crash
    control_panel.set_columns(['A', 'B', 'C'])
    control_panel.x_combo.setCurrentIndex(2)
    control_panel.y_combo.setCurrentIndex(0)
    control_panel.plot_type_combo.setCurrentIndex(1)
    qtbot.wait(50)


def test_plot_type_lowercase(control_panel):
    """Test that plot_type returns lowercase."""
    control_panel.plot_type_combo.setCurrentText('Histogram')
    assert control_panel.plot_type() == 'histogram'
    control_panel.plot_type_combo.setCurrentText('Box')
    assert control_panel.plot_type() == 'box'  # combo text 'Box' → lowercased
    # Implementation uses .lower()


def test_editable_label_combos(control_panel):
    """Test that label combos are editable."""
    assert control_panel.x_label_edit.isEditable()
    assert control_panel.y_label_edit.isEditable()
    assert control_panel.title_edit.isEditable()
    # User can type arbitrary text
    control_panel.x_label_edit.setCurrentText('Custom X')
    assert control_panel.options()['x_label'] == 'Custom X'