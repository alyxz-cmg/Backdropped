import cv2


class Camera:
    def __init__(self, index: int = 0) -> None:
        self._capture = cv2.VideoCapture(index)
        if not self._capture.isOpened():
            raise RuntimeError("Unable to open webcam.")

    def read_frame(self):
        ok, frame = self._capture.read()
        if not ok:
            return None
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def release(self) -> None:
        if self._capture.isOpened():
            self._capture.release()
