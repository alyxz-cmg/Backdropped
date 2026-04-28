from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtMultimedia import QMediaDevices
from PySide6.QtWidgets import (
    QComboBox,
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

        # --- Device Change Listener ---
        self._media_devices = QMediaDevices(self)
        self._media_devices.videoInputsChanged.connect(self._on_devices_changed)

        # --- Smart Camera Detection ---
        devices = QMediaDevices.videoInputs()
        num_devices = len(devices)
        best_qt_index = 0
        
        # Look for FaceTime or a non-iPhone/non-virtual camera
        for i, device in enumerate(devices):
            name = device.description().lower()
            if "facetime" in name or ("iphone" not in name and "virtual" not in name):
                best_qt_index = i
                break
                
        # Calculate the mirrored OpenCV index
        best_cv_index = (num_devices - 1) - best_qt_index if num_devices > 0 else 0

        # --- UI Setup ---
        self._camera_selector = QComboBox()
        self._populate_cameras(best_qt_index)
        self._camera_selector.currentIndexChanged.connect(self._on_camera_changed)
        
        controls = QHBoxLayout()
        controls.addWidget(self._camera_selector)
        controls.addWidget(self._record_button)

        layout = QVBoxLayout()
        layout.addWidget(self._label, stretch=1)
        layout.addWidget(self._status)
        layout.addLayout(controls)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self._camera = Camera(index=best_cv_index)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_frame)
        self._timer.start(30)

    def _populate_cameras(self, default_index: int = 0) -> None:
        """Query system for available cameras and populate the dropdown."""
        self._camera_selector.blockSignals(True)
        self._camera_selector.clear()
        
        video_devices = QMediaDevices.videoInputs()
        
        for device in video_devices:
            self._camera_selector.addItem(device.description())

        if not video_devices:
            self._camera_selector.addItem("No cameras found")
            self._camera_selector.setEnabled(False)
        else:
            self._camera_selector.setEnabled(True)
            self._camera_selector.setCurrentIndex(default_index)
            
        self._camera_selector.blockSignals(False)

    def _on_devices_changed(self) -> None:
        """Triggered whenever a camera is plugged in or disconnected."""
        current_name = self._camera_selector.currentText()
        
        self._populate_cameras()

        index = self._camera_selector.findText(current_name)

        if index >= 0:
            self._camera_selector.setCurrentIndex(index)
        else:
            self._camera_selector.setCurrentIndex(0)

    def _on_camera_changed(self, index: int) -> None:
        """Handle dropdown selection with an index-mapping fix."""
        if index >= 0:
            total_cameras = self._camera_selector.count()
            if total_cameras == 0:
                return
                
            corrected_index = (total_cameras - 1) - index
            
            self._timer.stop()
            self._camera.switch_source(corrected_index) 
            self._timer.start(30)
            
            self._status.setText(f"Switched to {self._camera_selector.currentText()}")

            QTimer.singleShot(5000, self._reset_status)

    def _reset_status(self) -> None:
        """Resets the status text based on the current state of the app."""
        if self._camera.is_recording:
            filename = self._camera._output_path.name if self._camera._output_path else "video"
            self._status.setText(f"Recording to {filename}")
        else:
            self._status.setText("Idle")

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