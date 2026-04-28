import cv2
import mediapipe as mp
import numpy as np


class Camera:
    def __init__(self, index: int = 0) -> None:
        self._capture = cv2.VideoCapture(index)
        if not self._capture.isOpened():
            raise RuntimeError("Unable to open webcam.")
        self._segmenter = mp.solutions.selfie_segmentation.SelfieSegmentation(
            model_selection=0
        )
        self._background = np.array([0, 255, 0], dtype=np.uint8)

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
        return composited

    def release(self) -> None:
        self._segmenter.close()
        if self._capture.isOpened():
            self._capture.release()
