"""
Unit tests for PlotController.
"""
import numpy as np
import pytest
from unittest.mock import Mock, patch
from src.plot.plot_controller import PlotController
from src.model.data_model import DataModel
from src.plot.plot_canvas import PlotCanvas


@pytest.fixture
def mock_data_model():
    """Create a mock DataModel."""
    model = Mock(spec=DataModel)
    model.get_column_data.return_value = np.array([1.0, 2.0, 3.0])
    return model


@pytest.fixture
def mock_plot_canvas():
    """Create a mock PlotCanvas."""
    canvas = Mock(spec=PlotCanvas)
    canvas.draw_plot = Mock()
    return canvas


@pytest.fixture
def controller(mock_data_model, mock_plot_canvas):
    return PlotController(mock_data_model, mock_plot_canvas)


def test_generate_plot_success(controller, mock_data_model, mock_plot_canvas):
    """Test successful plot generation."""
    # Set columns
    controller._x_column = 'X'
    controller._y_column = 'Y'
    controller._plot_type = 'scatter'
    # Call generate_plot with explicit columns
    controller.generate_plot(x_column='X', y_column='Y', plot_type='scatter')
    # Verify data retrieval
    mock_data_model.get_column_data.assert_any_call('X')
    mock_data_model.get_column_data.assert_any_call('Y')
    # Verify draw_plot called with correct args
    mock_plot_canvas.draw_plot.assert_called_once()
    call_args = mock_plot_canvas.draw_plot.call_args
    assert call_args[0][0].tolist() == [1.0, 2.0, 3.0]  # x_data
    assert call_args[0][1].tolist() == [1.0, 2.0, 3.0]  # y_data
    assert call_args[0][2] == 'scatter'
    # Options should include default grid, legend, labels
    kwargs = call_args[1]
    assert kwargs['grid'] == True
    assert kwargs['legend'] == False
    assert kwargs['x_label'] == 'X'
    assert kwargs['y_label'] == 'Y'
    assert 'Scatter of Y vs X' in kwargs['title']


def test_generate_plot_without_previous_selection(controller, mock_data_model, mock_plot_canvas):
    """Test that columns must be selected before generating plot."""
    controller._x_column = None
    controller._y_column = None
    with pytest.raises(ValueError, match='X and Y columns must be selected.'):
        controller.generate_plot()


def test_generate_plot_column_not_found(controller, mock_data_model):
    """Test error when column does not exist."""
    controller._x_column = 'X'
    controller._y_column = 'Y'
    mock_data_model.get_column_data.return_value = None
    with pytest.raises(ValueError, match='Column\\(s\\) not found'):
        controller.generate_plot()


def test_generate_plot_empty_data(controller, mock_data_model):
    """Test error when column data is empty."""
    controller._x_column = 'X'
    controller._y_column = 'Y'
    mock_data_model.get_column_data.return_value = np.array([])
    with pytest.raises(ValueError, match='Selected columns contain no data.'):
        controller.generate_plot()


def test_generate_plot_mismatched_lengths(controller, mock_data_model, mock_plot_canvas):
    """Test that arrays are trimmed to equal length."""
    x_data = np.array([1, 2, 3, 4])
    y_data = np.array([5, 6])
    mock_data_model.get_column_data.side_effect = [x_data, y_data]
    controller._x_column = 'X'
    controller._y_column = 'Y'
    controller.generate_plot()
    # Should trim to min length = 2
    call_args = mock_plot_canvas.draw_plot.call_args
    assert len(call_args[0][0]) == 2
    assert len(call_args[0][1]) == 2
    np.testing.assert_array_equal(call_args[0][0], [1, 2])
    np.testing.assert_array_equal(call_args[0][1], [5, 6])


def test_generate_plot_numeric_validation(controller, mock_data_model):
    """Test that non‑numeric data raises error for scatter/line/bar."""
    controller._x_column = 'X'
    controller._y_column = 'Y'
    controller._plot_type = 'scatter'
    # Mock data as string dtype
    x_data = np.array(['a', 'b', 'c'])
    y_data = np.array([1, 2, 3])
    mock_data_model.get_column_data.side_effect = [x_data, y_data]
    with pytest.raises(ValueError, match='Selected columns must be numeric'):
        controller.generate_plot()


def test_generate_plot_histogram_ignores_x(controller, mock_data_model, mock_plot_canvas):
    """Test histogram plot uses only y_data."""
    controller._x_column = 'X'
    controller._y_column = 'Y'
    controller._plot_type = 'histogram'
    x_data = np.array([1, 2, 3])  # will be ignored
    y_data = np.array([4, 5, 6])
    mock_data_model.get_column_data.side_effect = [x_data, y_data]
    controller.generate_plot()
    # The draw_plot call should still receive x_data (but histogram ignores it)
    call_args = mock_plot_canvas.draw_plot.call_args
    assert call_args[0][2] == 'histogram'
    # x_data passed as is (trimmed)
    np.testing.assert_array_equal(call_args[0][0], x_data)
    np.testing.assert_array_equal(call_args[0][1], y_data)


def test_generate_plot_box_ignores_x(controller, mock_data_model, mock_plot_canvas):
    """Test box plot uses only y_data."""
    controller._x_column = 'X'
    controller._y_column = 'Y'
    controller._plot_type = 'box'
    x_data = np.array([1, 2, 3])
    y_data = np.array([4, 5, 6])
    mock_data_model.get_column_data.side_effect = [x_data, y_data]
    controller.generate_plot()
    call_args = mock_plot_canvas.draw_plot.call_args
    assert call_args[0][2] == 'box'


def test_generate_plot_updates_selections(controller, mock_data_model, mock_plot_canvas):
    """Test that generate_plot updates stored selections when new columns provided."""
    controller._x_column = None
    controller._y_column = None
    controller._plot_type = 'scatter'
    controller.generate_plot(x_column='NewX', y_column='NewY', plot_type='line')
    assert controller._x_column == 'NewX'
    assert controller._y_column == 'NewY'
    assert controller._plot_type == 'line'
    mock_plot_canvas.draw_plot.assert_called_once()


def test_build_options(controller):
    """Test _build_options returns expected defaults."""
    controller._x_column = 'Xcol'
    controller._y_column = 'Ycol'
    controller._plot_type = 'scatter'
    opts = controller._build_options()
    assert opts == {
        'grid': True,
        'legend': False,
        'x_label': 'Xcol',
        'y_label': 'Ycol',
        'title': 'Scatter of Ycol vs Xcol',
    }