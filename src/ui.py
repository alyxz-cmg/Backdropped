from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QLabel, QMainWindow

from src.camera import Camera


class CameraWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Backdropped")
        self.resize(960, 720)

        self._label = QLabel("Starting camera...")
        self._label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self._label)

        self._camera = Camera()

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)
        self._timer.start(30)

    def _update_frame(self) -> None:
        frame = self._camera.read_frame()
        if frame is None:
            self._label.setText("Unable to read webcam frame.")
            return

        height, width, channels = frame.shape
        image = QImage(frame.data, width, height, channels * width, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        scaled = pixmap.scaled(
            self._label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self._label.setPixmap(scaled)

    def closeEvent(self, event) -> None:
        self._timer.stop()
        self._camera.release()
        super().closeEvent(event)
