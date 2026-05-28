"""
Poopee Desktop Pet — entry point.
Run:  python main.py
"""
import sys
from pathlib import Path

# Ensure the project root is on sys.path when run directly
sys.path.insert(0, str(Path(__file__).resolve().parent))

from PyQt6.QtWidgets import QApplication

from app.pet_widget import PetWidget


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # High-DPI support (Windows 10/11)
    try:
        from PyQt6.QtCore import Qt
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )
    except AttributeError:
        pass

    pet = PetWidget()
    pet.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
