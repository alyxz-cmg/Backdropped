import cv2
import numpy as np
import urllib.request
from pathlib import Path
from datetime import datetime

from mediapipe.tasks.python.vision import image_segmenter
from mediapipe.tasks.python.vision.core import image as mp_image

MODEL_URL = "https://storage.googleapis.com/mediapipe-assets/selfie_segmentation.tflite"
MODEL_FILENAME = "selfie_segmentation.tflite"
MODEL_DIR = Path("models")


class Camera:
    def __init__(self, index: int = 0) -> None:
        self._capture = cv2.VideoCapture(index, cv2.CAP_AVFOUNDATION)
        if not self._capture.isOpened():
            raise RuntimeError("Unable to open webcam.")

        self._capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self._capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        model_path = self._download_model()
        self._segmenter = image_segmenter.ImageSegmenter.create_from_model_path(
            str(model_path)
        )
        self._background = np.array([0, 255, 0], dtype=np.uint8)
        self._writer = None
        self._output_path = None

    def _download_model(self) -> Path:
        MODEL_DIR.mkdir(parents=True, exist_ok=True)
        model_path = MODEL_DIR / MODEL_FILENAME
        if not model_path.exists():
            urllib.request.urlretrieve(MODEL_URL, str(model_path))
        return model_path

    def read_frame(self):
        ok, frame = self._capture.read()
        if not ok:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = rgb_frame.shape[:2]

        # Run segmentation on a smaller frame to keep the live preview responsive.
        mask_input = cv2.resize(
            rgb_frame,
            (max(1, width // 2), max(1, height // 2)),
            interpolation=cv2.INTER_LINEAR,
        )
        mp_image_input = mp_image.Image(mp_image.ImageFormat.SRGB, mask_input)
        result = self._segmenter.segment(mp_image_input)

        if not result.confidence_masks:
            return rgb_frame

        mask = np.asarray(result.confidence_masks[0].numpy_view())
        if mask.ndim == 3 and mask.shape[-1] == 1:
            mask = mask[..., 0]
        if mask.dtype != np.float32:
            mask = mask.astype(np.float32)
        if mask.max() > 1.0:
            mask = mask / 255.0

        mask = cv2.resize(mask, (width, height), interpolation=cv2.INTER_LINEAR)
        foreground = mask > 0.5

        composited = np.full_like(rgb_frame, self._background)
        composited[foreground] = rgb_frame[foreground]

        if self._writer is not None:
            self._writer.write(cv2.cvtColor(composited, cv2.COLOR_RGB2BGR))

        return composited

    def start_recording(self) -> str:
        if self._writer is not None:
            return str(self._output_path)

        ok, frame = self._capture.read()
        if not ok:
            raise RuntimeError("Failed to read frame from camera.")
        height, width = frame.shape[:2]
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
