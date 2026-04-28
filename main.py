from PySide6.QtWidgets import QApplication

from src.ui import CameraWindow


def main() -> int:
    app = QApplication([])
    window = CameraWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
