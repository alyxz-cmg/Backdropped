from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.camera import Camera


class CameraWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Backdropped")
        self.resize(960, 720)

        self._label = QLabel("Starting camera...")
        self._label.setAlignment(Qt.AlignCenter)
        self._status = QLabel("Idle")
        self._status.setAlignment(Qt.AlignCenter)
        self._record_button = QPushButton("Start Recording")
        self._record_button.clicked.connect(self._toggle_recording)

        controls = QHBoxLayout()
        controls.addWidget(self._record_button)

        layout = QVBoxLayout()
        layout.addWidget(self._label, stretch=1)
        layout.addWidget(self._status)
        layout.addLayout(controls)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

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

    def _toggle_recording(self) -> None:
        if self._camera.is_recording:
            self._camera.stop_recording()
            self._record_button.setText("Start Recording")
            self._status.setText("Recording stopped")
            return

        output_path = self._camera.start_recording()
        self._record_button.setText("Stop Recording")
        self._status.setText(f"Recording to {output_path}")

    def closeEvent(self, event) -> None:
        self._timer.stop()
        self._camera.release()
        super().closeEvent(event)
