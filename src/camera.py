import cv2
import mediapipe as mp
import numpy as np
from pathlib import Path
from datetime import datetime


class Camera:
    def __init__(self, index: int = 0) -> None:
        self._capture = cv2.VideoCapture(index)
        if not self._capture.isOpened():
            raise RuntimeError("Unable to open webcam.")
        self._segmenter = mp.solutions.selfie_segmentation.SelfieSegmentation(
            model_selection=0
        )
        self._background = np.array([0, 255, 0], dtype=np.uint8)
        self._writer = None
        self._output_path = None

    def read_frame(self):
        ok, frame = self._capture.read()
        if not ok:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = rgb_frame.shape[:2]

        # Run segmentation on a smaller frame to keep the live preview responsive.
        mask_input = cv2.resize(rgb_frame, (width // 2, height // 2), interpolation=cv2.INTER_LINEAR)
        result = self._segmenter.process(mask_input)
        mask = cv2.resize(result.segmentation_mask, (width, height), interpolation=cv2.INTER_LINEAR)
        foreground = mask > 0.5

        composited = np.full_like(rgb_frame, self._background)
        composited[foreground] = rgb_frame[foreground]

        if self._writer is not None:
            self._writer.write(cv2.cvtColor(composited, cv2.COLOR_RGB2BGR))

        return composited

    def start_recording(self) -> str:
        if self._writer is not None:
            return str(self._output_path)

        width = int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        recordings_dir = Path("recordings")
        recordings_dir.mkdir(exist_ok=True)

        filename = datetime.now().strftime("backdropped-%Y%m%d-%H%M%S.mp4")
        self._output_path = recordings_dir / filename
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self._writer = cv2.VideoWriter(
            str(self._output_path),
            fourcc,
            30.0,
            (width, height),
        )
        if not self._writer.isOpened():
            self._writer.release()
            self._writer = None
            self._output_path = None
            raise RuntimeError("Unable to start video recording.")

        return str(self._output_path)

    def stop_recording(self) -> None:
        if self._writer is not None:
            self._writer.release()
            self._writer = None

    @property
    def is_recording(self) -> bool:
        return self._writer is not None

    def release(self) -> None:
        self.stop_recording()
        self._segmenter.close()
        if self._capture.isOpened():
            self._capture.release()
