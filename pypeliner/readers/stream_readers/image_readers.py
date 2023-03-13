"""
Image reader module, defines stream reading for images.
"""
from typing import Any

from pypeliner.exceptions import MissingDependency

try:
    import cv2
except ImportError:
    raise MissingDependency(
        "Image readers requires opencv-contrib-python==4.5.5.64 to be "
        "installed\nrun pip install opencv-contrib-python==4.5.5.64 to fix."
    )

from pypeliner.readers.base import BaseReader


class ImageStreamReader(BaseReader):
    def __init__(
        self, source: int = 0, break_on_fail: bool = True, break_key: int = 27
    ) -> None:
        super().__init__()
        self.cap = cv2.VideoCapture(source)
        self.break_on_fail = break_on_fail
        self.break_key = break_key

    def break_predicate(self, success: bool) -> bool:
        return (not success and self.break_on_fail) or cv2.waitKey(
            5
        ) & 0xFF == self.break_key

    def read(self) -> Any:
        while self.cap.isOpened():
            success, image = self.cap.read()

            if self.break_predicate(success):
                break

            yield image
