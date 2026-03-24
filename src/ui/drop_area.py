"""
Drag‑and‑drop area for CSV files.
"""
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPainter, QPen, QColor, QFont
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class DropArea(QWidget):
    """A widget that accepts drag‑and‑drop of CSV files."""

    # Signal emitted when a file is dropped; carries the file path
    file_dropped = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self._is_dragging = False
        self._init_ui()

    def _init_ui(self):
        """Set up visual appearance."""
        self.setMinimumHeight(150)
        self.setMaximumHeight(250)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Icon placeholder (text)
        icon_label = QLabel('📄')
        icon_label.setAlignment(Qt.AlignCenter)
        font = icon_label.font()
        font.setPointSize(48)
        icon_label.setFont(font)
        layout.addWidget(icon_label)

        # Hint text
        hint_label = QLabel(
            'Drag and drop a CSV file here\n'
            'or click "Open" from the File menu.'
        )
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setWordWrap(True)
        font = hint_label.font()
        font.setPointSize(11)
        hint_label.setFont(font)
        hint_label.setStyleSheet('color: gray;')
        layout.addWidget(hint_label)

        # Supported formats label
        formats_label = QLabel('Supported: .csv, .txt (comma, tab, semicolon)')
        formats_label.setAlignment(Qt.AlignCenter)
        formats_label.setStyleSheet('color: darkGray; font-size: 9pt;')
        layout.addWidget(formats_label)

        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #aaa;
                border-radius: 10px;
                background-color: #f8f8f8;
            }
            DropArea:hover {
                border-color: #0078d7;
                background-color: #f0f7ff;
            }
        """)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Accept the drag if it contains URLs (files)."""
        if event.mimeData().hasUrls():
            # Check if any URL is a CSV file
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(('.csv', '.txt')):
                    event.acceptProposedAction()
                    self._is_dragging = True
                    self.update()
                    return
        event.ignore()

    def dragLeaveEvent(self, event) -> None:
        """Reset dragging state when drag leaves."""
        self._is_dragging = False
        self.update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event: QDropEvent) -> None:
        """Handle the dropped file."""
        self._is_dragging = False
        self.update()
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.lower().endswith(('.csv', '.txt')):
                    self.file_dropped.emit(file_path)
                    event.acceptProposedAction()
                    return
        event.ignore()

    def paintEvent(self, event):
        """Custom paint to highlight when dragging."""
        super().paintEvent(event)
        if self._is_dragging:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            pen = QPen(QColor(0, 120, 215), 3, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRoundedRect(self.rect().adjusted(5, 5, -5, -5), 10, 10)
            painter.end()