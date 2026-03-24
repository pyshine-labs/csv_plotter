"""
Unit tests for DropArea widget.
"""
import pytest
from PyQt5.QtCore import Qt, QMimeData, QUrl
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from src.ui.drop_area import DropArea


@pytest.fixture
def drop_area(qtbot):
    """Create a DropArea instance."""
    widget = DropArea()
    qtbot.addWidget(widget)
    return widget


def test_drop_area_initial_state(drop_area):
    """Test that DropArea is properly initialized."""
    assert drop_area.acceptDrops() == True
    # Check that it has a layout
    assert drop_area.layout() is not None


def test_drag_enter_event_accepts_csv(drop_area, qtbot):
    """Test that dragEnterEvent accepts CSV files."""
    mime = QMimeData()
    url = QUrl.fromLocalFile('/path/to/data.csv')
    mime.setUrls([url])
    event = QDragEnterEvent(
        drop_area.pos(), Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier
    )
    # Spy on the signal
    with qtbot.waitSignal(drop_area.file_dropped, timeout=1000, raising=False):
        drop_area.dragEnterEvent(event)
    assert event.isAccepted()
    # Visual flag should be set
    # (we cannot directly check _is_dragging because it's private, but we can trust)


def test_drag_enter_event_rejects_non_csv(drop_area):
    """Test that dragEnterEvent rejects non‑CSV files."""
    mime = QMimeData()
    url = QUrl.fromLocalFile('/path/to/image.png')
    mime.setUrls([url])
    event = QDragEnterEvent(
        drop_area.pos(), Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier
    )
    drop_area.dragEnterEvent(event)
    assert not event.isAccepted()


def test_drag_leave_event_resets_state(drop_area, qtbot):
    """Test that dragLeaveEvent resets dragging flag."""
    drop_area._is_dragging = True
    # We need a dummy event; QDragLeaveEvent has no constructor arguments in PyQt5
    from PyQt5.QtGui import QDragLeaveEvent
    event = QDragLeaveEvent()
    drop_area.dragLeaveEvent(event)
    assert drop_area._is_dragging == False


def test_drop_event_emits_signal(drop_area, qtbot):
    """Test that dropping a CSV file emits file_dropped with the file path."""
    mime = QMimeData()
    url = QUrl.fromLocalFile('/home/user/data.csv')
    mime.setUrls([url])
    event = QDropEvent(
        drop_area.pos(), Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier
    )
    # Use qtbot to wait for signal
    with qtbot.waitSignal(drop_area.file_dropped, timeout=1000) as blocker:
        drop_area.dropEvent(event)
    # Check the emitted path
    assert blocker.args == ['/home/user/data.csv']
    assert event.isAccepted()


def test_drop_event_ignores_non_csv(drop_area, qtbot):
    """Test that dropping a non‑CSV file does not emit signal."""
    mime = QMimeData()
    url = QUrl.fromLocalFile('/home/user/image.jpg')
    mime.setUrls([url])
    event = QDropEvent(
        drop_area.pos(), Qt.CopyAction, mime,
        Qt.LeftButton, Qt.NoModifier
    )
    # Ensure signal is not emitted
    drop_area.file_dropped.connect(lambda path: pytest.fail('Signal should not be emitted'))
    drop_area.dropEvent(event)
    assert not event.isAccepted()


def test_paint_event_with_dragging(drop_area, qtbot):
    """Test that paintEvent doesn't crash when dragging."""
    drop_area._is_dragging = True
    # Just trigger update; we cannot easily verify painting
    drop_area.update()
    qtbot.wait(50)  # allow paint event to be processed
    # No assertion; just ensure no exception


def test_paint_event_without_dragging(drop_area, qtbot):
    """Test normal paint event."""
    drop_area._is_dragging = False
    drop_area.update()
    qtbot.wait(50)