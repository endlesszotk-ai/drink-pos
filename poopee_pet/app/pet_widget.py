import random
from pathlib import Path

from PyQt6.QtCore import QPoint, Qt, QTimer
from PyQt6.QtGui import QAction, QCursor, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QMenu, QWidget

from . import config as cfg
from .ai import AIProvider, get_provider
from .bubble_widget import BubbleWidget
from .chat_dialog import ask_user

_ROOT = Path(__file__).resolve().parent.parent
_SPRITE_DIR = _ROOT / "assets" / "sprites"

SPRITES: dict[str, str] = {
    "idle_sleepy": "idle_sitting_sleepy.png",
    "idle_front": "idle_sitting_front.png",
    "walk": "walk_pose.png",
    "stand": "stand_alert.png",
    "surprised": "surprised_lie.png",
    "peek": "peek_head.png",
    "sleep_side": "sleep_side.png",
    "curl_sleep": "curl_sleep.png",
    "sleep_long_left": "sleep_long_left.png",
    "sleep_low_right": "sleep_low_right.png",
    "sleep_low_left": "sleep_low_left.png",
}

_IDLE_POOL = ["idle_sleepy", "idle_front", "stand", "walk", "sleep_side"]


class PetWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._config = cfg.load()
        self._ai: AIProvider = get_provider(_ROOT)
        self._drag_pos: QPoint | None = None
        self._pose: str = (
            self._config["pose"] if self._config["pose"] in SPRITES else "idle_sleepy"
        )
        self._scale: float = float(self._config.get("scale", 1.0))
        self._always_on_top: bool = bool(self._config.get("always_on_top", True))

        self._label = QLabel(self)
        self._label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._bubble = BubbleWidget()

        self._apply_flags()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._load_sprite(self._pose)
        self.move(int(self._config["x"]), int(self._config["y"]))

        self._idle_timer = QTimer(self)
        self._idle_timer.timeout.connect(self._random_idle)
        self._idle_timer.start(12_000)

    # ── Window flags ─────────────────────────────────────────────────────────

    def _apply_flags(self) -> None:
        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self._always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)

    # ── Sprite ───────────────────────────────────────────────────────────────

    def _load_sprite(self, pose: str) -> None:
        self._pose = pose
        path = _SPRITE_DIR / SPRITES[pose]
        pixmap = QPixmap(str(path))
        if pixmap.isNull():
            raise FileNotFoundError(f"Sprite not found: {path}")
        width = max(80, int(pixmap.width() * self._scale))
        pixmap = pixmap.scaledToWidth(width, Qt.TransformationMode.SmoothTransformation)
        self._label.setPixmap(pixmap)
        self._label.resize(pixmap.size())
        self.resize(pixmap.size())
        self._persist()

    # ── Mouse events ─────────────────────────────────────────────────────────

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
        event.accept()

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton and self._drag_pos is not None:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        event.accept()

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        self._persist()
        event.accept()

    def mouseDoubleClickEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._open_chat()

    # ── Context menu ─────────────────────────────────────────────────────────

    def contextMenuEvent(self, event) -> None:
        menu = QMenu(self)

        pose_menu = menu.addMenu("Change Pose")
        for name in SPRITES:
            action = QAction(name, self)
            action.triggered.connect(lambda checked=False, p=name: self._load_sprite(p))
            pose_menu.addAction(action)

        scale_menu = menu.addMenu("Scale")
        for label, value in [("75%", 0.75), ("100%", 1.0), ("125%", 1.25), ("150%", 1.5)]:
            action = QAction(label, self)
            action.triggered.connect(lambda checked=False, v=value: self._set_scale(v))
            scale_menu.addAction(action)

        top_action = QAction(
            "Always on Top  ✓" if self._always_on_top else "Always on Top", self
        )
        top_action.triggered.connect(self._toggle_always_on_top)
        menu.addAction(top_action)

        chat_action = QAction("Chat with Poopee", self)
        chat_action.triggered.connect(self._open_chat)
        menu.addAction(chat_action)

        menu.addSeparator()
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)
        menu.addAction(quit_action)

        menu.exec(QCursor.pos())

    # ── Actions ──────────────────────────────────────────────────────────────

    def _set_scale(self, scale: float) -> None:
        self._scale = scale
        self._load_sprite(self._pose)

    def _toggle_always_on_top(self) -> None:
        self._always_on_top = not self._always_on_top
        self._apply_flags()
        self.show()
        self._persist()

    def _open_chat(self) -> None:
        user_text = ask_user(self)
        if not user_text:
            return
        next_pose = "peek" if self._pose != "peek" else "idle_front"
        self._load_sprite(next_pose)
        try:
            reply = self._ai.ask(user_text)
        except Exception as exc:
            reply = f"เมี๊ยว… API มีปัญหา: {exc}"
        self._bubble.say(reply, self.geometry().topLeft())

    def _random_idle(self) -> None:
        if random.random() < 0.45:
            self._load_sprite(random.choice(_IDLE_POOL))

    # ── Persistence ──────────────────────────────────────────────────────────

    def _persist(self) -> None:
        self._config.update(
            {
                "x": self.x(),
                "y": self.y(),
                "scale": self._scale,
                "pose": self._pose,
                "always_on_top": self._always_on_top,
            }
        )
        cfg.save(self._config)

    def closeEvent(self, event) -> None:
        self._persist()
        self._bubble.close()
        super().closeEvent(event)
