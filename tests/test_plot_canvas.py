"""
Unit tests for PlotCanvas.
"""
import numpy as np
import pytest
from src.plot.plot_canvas import PlotCanvas


@pytest.fixture
def plot_canvas(qtbot):
    """Create a PlotCanvas instance."""
    canvas = PlotCanvas()
    qtbot.addWidget(canvas)
    return canvas


def test_initial_state(plot_canvas):
    """Test that canvas initializes with placeholder."""
    assert plot_canvas.figure is not None
    assert plot_canvas.axes is not None
    # Initially there should be a text placeholder
    texts = plot_canvas.axes.texts
    assert len(texts) > 0
    assert 'No plot data' in texts[0].get_text()


def test_clear_plot(plot_canvas):
    """Test clear_plot method."""
    plot_canvas.clear_plot()
    # Should still have placeholder text
    texts = plot_canvas.axes.texts
    assert any('No plot data' in t.get_text() for t in texts)


def test_draw_plot_scatter(plot_canvas):
    """Test drawing a scatter plot."""
    x = np.array([1, 2, 3, 4])
    y = np.array([5, 6, 7, 8])
    plot_canvas.draw_plot(x, y, 'scatter')
    # Should have collections (scatter)
    assert len(plot_canvas.axes.collections) > 0
    # No exception


def test_draw_plot_line(plot_canvas):
    """Test drawing a line plot."""
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_canvas.draw_plot(x, y, 'line')
    # Should have lines
    assert len(plot_canvas.axes.lines) > 0


def test_draw_plot_bar(plot_canvas):
    """Test drawing a bar plot."""
    x = np.array([1, 2, 3])
    y = np.array([10, 20, 30])
    plot_canvas.draw_plot(x, y, 'bar')
    # Should have patches
    assert len(plot_canvas.axes.patches) > 0


def test_draw_plot_histogram(plot_canvas):
    """Test drawing a histogram."""
    x = np.array([])  # ignored
    y = np.array([1, 2, 2, 3, 3, 3, 4])
    plot_canvas.draw_plot(x, y, 'histogram')
    # Should have patches (bars)
    assert len(plot_canvas.axes.patches) > 0


def test_draw_plot_box(plot_canvas):
    """Test drawing a box plot."""
    x = np.array([])
    y = np.array([1, 2, 3, 4, 5])
    plot_canvas.draw_plot(x, y, 'box')
    # Should have boxplot elements
    assert len(plot_canvas.axes.lines) > 0  # boxplot creates lines


def test_draw_plot_with_options(plot_canvas):
    """Test drawing with custom options (grid, labels, title)."""
    x = np.array([1, 2])
    y = np.array([3, 4])
    plot_canvas.draw_plot(x, y, 'scatter',
                          grid=False,
                          x_label='X Axis',
                          y_label='Y Axis',
                          title='Test Plot',
                          legend=True)
    # Verify options applied (hard to test directly)
    # No assertion; just ensure no crash


def test_save_plot(tmp_path, plot_canvas):
    """Test saving plot to file."""
    # Draw something first
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 6])
    plot_canvas.draw_plot(x, y, 'line')
    # Save to temporary file
    file_path = tmp_path / 'test_plot.png'
    plot_canvas.save_plot(str(file_path))
    assert file_path.exists()
    # File should be non‑empty
    assert file_path.stat().st_size > 0


def test_toolbar_methods(plot_canvas):
    """Test convenience methods for toolbar actions (should not crash)."""
    plot_canvas.zoom_in()
    plot_canvas.zoom_out()
    plot_canvas.home()
    plot_canvas.pan()
    # No assertions; just ensure they run


def test_unknown_plot_type_ignored(plot_canvas):
    """If plot_type is unknown, should default to scatter? Actually no match."""
    # The draw_plot uses if‑elif; unknown type will skip all branches,
    # resulting in empty axes. That's fine.
    x = np.array([1, 2])
    y = np.array([3, 4])
    plot_canvas.draw_plot(x, y, 'unknown')
    # No collections, lines, patches
    # Not testing anything specific.