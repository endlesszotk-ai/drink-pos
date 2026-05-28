from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtWidgets import QLabel


class BubbleWidget(QLabel):
    def __init__(self) -> None:
        super().__init__(None)
        self.setWindowFlags(
            Qt.WindowType.Tool
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet(
            """
            QLabel {
                background: rgba(255, 255, 255, 240);
                color: #111111;
                border: 2px solid #333333;
                border-radius: 14px;
                padding: 10px 16px;
                font-size: 14px;
                font-family: "Segoe UI", "TH Sarabun New", Tahoma, sans-serif;
            }
            """
        )
        self.setWordWrap(True)
        self.setMinimumWidth(180)
        self.setMaximumWidth(360)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def say(self, text: str, pet_top_left: QPoint, duration_ms: int = 8000) -> None:
        self.setText(text)
        self.adjustSize()
        x = pet_top_left.x()
        y = max(20, pet_top_left.y() - self.height() - 16)
        self.move(x, y)
        self.show()
        self.raise_()
        self._timer.start(duration_ms)
