from PyQt6.QtWidgets import QInputDialog, QWidget


def ask_user(parent: QWidget) -> str | None:
    """Show a simple chat input dialog. Returns stripped text or None."""
    text, ok = QInputDialog.getText(parent, "คุยกับโปสตี้", "อยากบอกอะไรโปสตี้?")
    if ok and text.strip():
        return text.strip()
    return None
